from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
from .models import Product

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
        if soup.find("span", {"class": "in-stock stock-blob product-qty-blob"}):
            in_stock = True
        name = soup.find("h1", {"class": "h1meoane h150u3pp"}).text
        url = soup.find('link', {'rel': 'canonical'})['href']
        data = {
        'name': name,
        'website': 'Inet',
        'availability': in_stock,
        'url': url,
        'price': 0,
        }
        return data


    def check_item_in_stock_komplett(self, page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        in_stock = False
        if soup.find("div", {"class": "stockstatus"}):
            in_stock = True
        name = soup.find('span', {'data-bind': 'text: webtext1'}).text
        data = {
        'name': name,
        'website': 'Komplett',
        'availability': in_stock,
        'url': '',
        'price': 0,
        }
        return data
        


    def check_item_in_stock_netonnet(self, page_html):
        soup = BeautifulSoup(page_html, 'html5lib')
        in_stock = False
        if soup.find("div", {"class": "stock-status"}):
            in_stock = True
        data = {
        'name': 'PS5',
        'website': 'Netonnet',
        'availability': in_stock,
        'url': '',
        'price': 0,
        }
        return data

    # special case, uses webhallen's own server search API
    def check_item_in_stock_webhallen(self):
        BASE = "https://www.webhallen.com/api/product/"
        product_ids = {"320479", "300815"}
        for product_id in product_ids:
            req = requests.get(BASE + product_id, headers=self.headers)
            response_data = req.json()
            product = response_data["product"]
            in_stock = product["stock"]["web"] > 0
            if in_stock:
                print(product["name"])
                print(product["price"]["price"])
        data = {
        'name': 'Playstatiooon',
        'website': 'Webhallen',
        'availability': in_stock,
        'url': '',
        'price': 0,
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
        urls = {"https://www.inet.se/produkt/6609862/sony-playstation-5-digital-edition", "https://www.inet.se/produkt/6609649/sony-playstation-5", "https://www.komplett.se/product/1111557/gaming/playstation/playstation-5-ps5", "https://www.komplett.se/product/1161553/gaming/playstation/playstation-5-digital-edition-ps5", "https://www.webhallen.com/se/product/346166-MSI-Optix-G251F-25-IPS-1080p-1ms-165Hz-DP-HDMI-HDR-G-Sync", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5/1012886.14413/", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-digital-edition/1013477.14413/" }
        #testUrls = {"https://www.inet.se/produkt/5412819/d-link-e15-ax1500-mesh-range-extender",
                #"https://www.komplett.se/product/1161554/gaming/tillbehor-till-spelkonsoler/playstation-5-hd-camera",
               # "https://www.webhallen.com/se/product/346166-MSI-Optix-G251F-25-IPS-1080p-1ms-165Hz-DP-HDMI-HDR-G-Sync",
                #"https://www.netonnet.se/art/gaming/spel-och-konsol/xbox/xbox-konsol/microsoft-xbox-series-s/1012885.14412/"}

        scraped_data = []

        for url in urls:
            page_html = self.get_page_html(url)

            if "inet" in url:
                scraped_data.append(self.check_item_in_stock_inet(page_html))

            elif "komplett" in url:
                scraped_data.append(self.check_item_in_stock_komplett(page_html))


            elif "webhallen" in url:
                scraped_data.append(self.check_item_in_stock_webhallen())


            elif "netonnet" in url:
                scraped_data.append(self.check_item_in_stock_netonnet(page_html))
        self.save_to_database(scraped_data)
        return 1