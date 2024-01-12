import time
from playwright.sync_api import sync_playwright


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
        case "2":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-inf03-ee09-programowanie-bazy-danych/"
        case "3":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-sprzet-urzadzenia-peryferyjne/"
        case "4":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-systemy-operacyjne-programy/"
        case "5":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-sieci-komputerowe/"
        case "6":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-bazy-danych-sql-mysql/"
        case "7":
            url = "https://egzamin-informatyk.pl/jedno-pytanie-html-css-js-php/"

    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            mouse = page.mouse
            goToSite(page,mouse, url)
            while(True):
                scrapeQuestion(page)
                time.sleep(0.5)




def goToSite(page,mouse, url):
    page.goto(url)

    mouse.wheel(0, 1260)



def scrapeQuestion(page):

    page.locator("span#losujnowe").click()

    id = page.locator('h3').text_content().replace(" Pytanie nr ", "").replace(" - Wskaż poprawną odpowiedź!", "")


    question = page.locator('div.tresc').text_content()

    odpa = page.locator('div#odpa').text_content().replace("A. ", "")
    odpb = page.locator('div#odpb').text_content().replace("B. ", "")
    odpc = page.locator('div#odpc').text_content().replace("C. ", "")
    odpd = page.locator('div#odpd').text_content().replace("D. ", "")


    print(id + "\n" + question + "\n" +odpa + "\n" + odpb + "\n" + odpc + "\n" + odpd )
    if page.locator('div.obrazek').is_visible():
        print("Znaleziono obrazek")
        image =  page.locator("div.obrazek").inner_html().replace('<img class="img-responsive" src="..','https://egzamin-informatyk.pl').replace('" alt="">','')
        print(image)
        
   

    page.locator('div#odpa').click()

    match page.locator('div.odpgood').text_content()[0]:
        case "A":
            print("Poprawna odpowiedź: A")
        case "B":
            print("Poprawna odpowiedź: B")
        case "C":
            print("Poprawna odpowiedź: C")
        case "D":
            print("Poprawna odpowiedź: D")


    

if __name__ == "__main__":
    main()