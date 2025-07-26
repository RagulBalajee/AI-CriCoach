# scripts/data_scraper.py
import requests
from bs4 import BeautifulSoup

def get_live_score():
    url = "https://www.cricbuzz.com/live-cricket-scores"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    score = soup.find("div", class_="cb-scr-wll-chvrn cb-hmscg-bat-live")
    return score.text.strip() if score else "Score not found"

if __name__ == "__main__":
    print(get_live_score())
