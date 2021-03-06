"""
Parser for ceneo.pl price comparator.
Output is being sent via Telegram Bot API

Example usage:

	python3.7 scrapper.py "Samsung s10e"
"""

import requests
from bs4 import BeautifulSoup
import re
import argparse
import tg_helper

def get_data_for_product(product="Samsung+s10e"):
	CENEO_URL = "https://www.ceneo.pl"
	CENEO_SEARCH_URL = f"{CENEO_URL}/;szukaj-{PRODUCT}" 

	try:
		response = requests.get(CENEO_SEARCH_URL)
		if response.status_code != 200:
			print(f"Error: {response.text}")
			raise requests.exceptions.ConnectionError
	except Exception as e:
		print(f"An error occured")
		exit(0)
		
	html = response.text

	soup = BeautifulSoup(html, 'html.parser')

	alert = soup.find("div", attrs={'class': "alert"})
	if alert is not None:
		print("Not found")
		exit(0)

	entries = {}
	for product in soup.findAll(attrs={'class': re.compile(r".*cat-prod-row__content.*")}):
		product_desc = product.find("div", attrs={'class': "cat-prod-row__desc"})
		product_price = product.find("div", attrs={'class': "cat-prod-row__price"})
		try:
			product_name = product_desc.find("strong", attrs={"class": "cat-prod-row__name"}).find('a').text
		except AttributeError:
			continue

		try:
			product_href = product_price.find("a", attrs={'class': "go-to-product"}).get("href")
		except AttributeError:
			continue
		product_price_value = product_price.find("span", attrs={'class': "value"})
		
		product_url = f"{CENEO_URL}{product_href}"
		entries[product_url] = {
			"name": product_name,
			"price": product_price_value.text
		}
	return entries
	
def send_info(entries):
	CENEO_URL = "https://www.ceneo.pl"
	product_message = ""	
	for product_url in list(entries)[0:6]:
		product_message += f"[{entries[product_url]['name']}]({product_url}) - `{entries[product_url]['price']} PLN`\n"

	telegram_message = 	f"""
	-------------------------------------
	Latest prices for *{args.product}* from [Ceneo]({CENEO_URL})
	{product_message}
	--------------------------------------
	"""

	tg_helper.send(telegram_message, parse_mode="Markdown")
	
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('product', type=str,
						help='Name of the product to find')
	args = parser.parse_args()
	PRODUCT = args.product.replace(' ','+')
	entries = get_data_for_product(PRODUCT)
	send_info(entries)
