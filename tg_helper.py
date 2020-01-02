import requests
from os import getenv

TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
TG_USER_ID = getenv("TG_USER_ID")
TG_URL = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

def send(text, parse_mode="html"):
	data = {
		"chat_id": int(TG_USER_ID),
		"text": text,
		"parse_mode": parse_mode
	}
	requests.post(TG_URL, data=data)
	