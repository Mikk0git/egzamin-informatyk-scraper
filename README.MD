# Web Scraping Bot for egzamin-informatyk.pl

This Python bot is designed to scrape questions from the website [egzamin-informatyk.pl](https://egzamin-informatyk.pl/) and store them in an SQLite database

## Usage

- install required packages

```
pip install -r requirements.txt
```

- install playwright's browser

```
playwright install
```

- run the script

```
python app.py
```

It picks a random question, saves it with the answers, and repeats the process
