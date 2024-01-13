import time
from playwright.sync_api import sync_playwright
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey,String, Boolean, Column, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Questions(Base):
    __tablename__ = 'questions'
    id = Column(String, primary_key=True)#i know it isnt normilised but it should be fine
    question = Column(String)
    image = Column(String)
    examType = Column(String)

    def __init__(self,id, question, image, examType):
        self.id = id
        self.question = question
        self.image = image
        self.examType = examType

    def __repr__(self):
        return f"ID: {self.id} Question: {self.question} Image: {self.image} Exam: {self.examType}"

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    answer = Column(String)
    isCorrect = Column(Boolean)
    question_id = Column(String, ForeignKey('questions.id'))

    def __init__(self, answer, isCorrect, question_id):
        self.answer = answer
        self.isCorrect = isCorrect
        self.question_id = question_id

    def __repr__(self):
        return f"ID: {self.id} Answer: {self.answer} Correct: {self.isCorrect} Question ID: {self.question_id}"

engine = create_engine('sqlite:///egzamin.db',echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()




def main():
    print("---egzamin-informatyk.pl---")
    print("Dostępne egzaminy:")
    print("1. EE.08 / INF.02")
    print("2. EE.09 / INF.03 / E.14")
    print("3. Sprzet komputerowy")
    print("4. Systemy operacyjne")
    print("5. Sieci komputerowe")
    print("6. Bazy danych i SQL")
    print("7. HTML, CSS, JS i PHP")

    examNumber = input("Wybierz egzamin: ")
    
    url = ""
    match examNumber:
        case "1":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-inf02-ee08-sprzet-systemy-sieci/"
            examType = "EE.08 / INF.02"
            idType = 'A' 
        case "2":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-inf03-ee09-programowanie-bazy-danych/"
            examType = "EE.09 / INF.03 / E.14"
            idType = 'B'
        case "3":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-sprzet-urzadzenia-peryferyjne/"
            examType = "Sprzet komputerowy"
            idType = 'C'
        case "4":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-systemy-operacyjne-programy/"
            examType = "Systemy operacyjne"
            idType = 'D'
        case "5":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-sieci-komputerowe/"
            examType = "Sieci komputerowe"
            idType = 'E'
        case "6":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-bazy-danych-sql-mysql/"
            examType = "Bazy danych i SQL"
            idType = 'F'
        case "7":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-html-css-js-php/"
            examType = "HTML, CSS, JS i PHP"
            idType = 'G'

    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            mouse = page.mouse
            goToSite(page,mouse, url)
            while(True):
                scrapeQuestion(page,examType,idType)
                time.sleep(0.7)




def goToSite(page,mouse, url):
    page.goto(url)

    mouse.wheel(0, 1260)



def scrapeQuestion(page,examType,idType):

    # page.locator("span#losujnowe").click()

    id =  page.locator('h3').text_content().replace(" Pytanie nr ", "").replace(" - Wskaż poprawną odpowiedź!", "") + idType
    
    if session.query(Questions).filter(Questions.id == id).first() or 'Nie' in id or 'Tak' in id:
        page.locator("span#losujnowe").click()
        return


    question = page.locator('div.tresc').text_content()

    odpa = page.locator('div#odpa').text_content().replace("A. ", "")
    odpb = page.locator('div#odpb').text_content().replace("B. ", "")
    odpc = page.locator('div#odpc').text_content().replace("C. ", "")
    odpd = page.locator('div#odpd').text_content().replace("D. ", "")


    print(id + "\n" + question + "\n" +odpa + "\n" + odpb + "\n" + odpc + "\n" + odpd )

    image = ''
    if page.locator('div.obrazek').is_visible():
        print("Znaleziono obrazek")
        image =  page.locator("div.obrazek").inner_html().replace('<img class="img-responsive" src="..','https://egzamin-informatyk.pl').replace('" alt="">','')
        print(image)
    
    #Add question to DB
    question = Questions(id,question,image,examType)
    session.add(question)
    
    answers = [
        Answers(odpa, True, id),
        Answers(odpb, False, id),
        Answers(odpc, False, id),
        Answers(odpd, False, id)
    ] 

    page.locator('div#odpa').click()

    match page.locator('div.odpgood').text_content()[0]:
        case "A":
            print("Poprawna odpowiedź: A")
            answers[0].isCorrect = True
        case "B":
            print("Poprawna odpowiedź: B")
            answers[1].isCorrect = True
        case "C":
            print("Poprawna odpowiedź: C")
            answers[2].isCorrect = True
        case "D":
            print("Poprawna odpowiedź: D")
            answers[3].isCorrect = True

    session.add_all(answers)
    
    session.commit()
    page.locator("span#losujnowe").click()


    

if __name__ == "__main__":
    main()