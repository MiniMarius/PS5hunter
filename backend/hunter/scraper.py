from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
from .models import Product
from .models import Website
from .models import TagData
import re
class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Accept-Language': 'en-US'}
        
        
    def get_page_html(self, product_url):
        page = requests.get(product_url, headers=self.headers)
        print(page.status_code)
        return page.content


    def check_item_in_stock_inet(self, page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        in_stock = False
        if soup.find('span', class_=['s1ys0gx5', 's14li1pv']):
            in_stock = True
        name = soup.find("h1", {"class": "h1meoane h150u3pp"}).text
        url = soup.find('link', {'rel': 'canonical'})['href']
        price_with_spaces = soup.find('span', {'class': 'bp5wbcj l1gqmknm'}).text
        price = price_with_spaces.replace('\xa0', '').replace('kr', '')
        data = {
        'name': name,
        'website': 'Inet',
        'availability': in_stock,
        'url': url,
        'price': price,
        }
        return data


    def check_item_in_stock_komplett(self, page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        in_stock = False
        if soup.find("div", {"class": "stockstatus"}):
            in_stock = True
        name = soup.find('span', {'data-bind': 'text: webtext1'}).text
        price_tag = soup.find('span', {'class': 'product-price-now'})
        price_number = 0
        if price_tag:
            price_text = price_tag.text.strip()
            price_number = ''.join(filter(str.isdigit, price_text))
        link_tag = soup.find('link', {'rel': 'canonical'})
        url = link_tag['href']
        data = {
        'name': name,
        'website': 'Komplett',
        'availability': in_stock,
        'url': url,
        'price': price_number,
        }
        return data
        


    def check_item_in_stock_netonnet(self, page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        in_stock = False
        if soup.find("div", {"class": "stock-status"}):
            in_stock = True
        name = soup.find('meta', {'property': 'og:title'})['content']
        price_soup = soup.find('div', class_='price-big')
        price = 0
        if price_soup:
            price_text = price_soup.text
            price = int(''.join(filter(str.isdigit, price_text)))
        url = soup.find('link', {'rel': 'canonical'})['href']
        data = {
        'name': name,
        'website': 'Netonnet',
        'availability': in_stock,
        'url': url,
        'price': price,
        }
        return data

    # special case, uses webhallen's own server search API
    def check_item_in_stock_webhallen(self):
        BASE = "https://www.webhallen.com/api/product/"
        product_id = "320479"
        req = requests.get(BASE + product_id, headers=self.headers)
        response_data = req.json()
        product = response_data["product"]
        name = product["variants"]["list"][0]["name"]
        price = float(product["variants"]["list"][0]["price"]["price"])
        availability = product["variants"]["list"][0]["stock"]["web"] > 0
        data = {
        'name': name,
        'website': 'Webhallen',
        'availability': availability,
        'url': '',
        'price': price,
        }
        return data        
    
    def save_to_database(self, data):
        for entry in data:
            product_data = Product(
                name=entry['name'],
                website=entry['website'],
                availability=entry['availability'],
                url=entry['url'],
                price=entry['price']
                )
            product_data.save()


    def check_inventory(self):
        urls = {"https://www.inet.se/produkt/6609862/sony-playstation-5-digital-edition", "https://www.inet.se/produkt/6609649/sony-playstation-5", "https://www.komplett.se/product/1111557/gaming/playstation/playstation-5-ps5", "https://www.komplett.se/product/1161553/gaming/playstation/playstation-5-digital-edition-ps5", "https://www.webhallen.com/se/product/346166-MSI-Optix-G251F-25-IPS-1080p-1ms-165Hz-DP-HDMI-HDR-G-Sync", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-c-chassi/1027489.14413/", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-standard-god-of-war-ragnarok-voucher/1027712.14413/" }
        print("yes")
        return 1