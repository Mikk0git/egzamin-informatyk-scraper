# from playwright.sync_api import Page, expect


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

    



# def goToSite(page: Page, url):
#     page.goto(url)
    

if __name__ == "__main__":
    main()