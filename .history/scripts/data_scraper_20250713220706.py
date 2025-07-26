import requests
from bs4 import BeautifulSoup
import json

def get_live_match(match_id):
    # replace with official API or Cricbuzz scraping logic
    url = f"https://api.example.com/match/{match_id}" 
    resp = requests.get(url)
    return resp.json()

def get_live_score_html():
    url = "https://www.cricbuzz.com/live-cricket-scores"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    score = soup.find("div", {"class": "cb-scr-wll-chvrn cb-hmscg-bat-live"})
    return score.text.strip() if score else None

if __name__ == "__main__":
    print(get_live_score_html())
