from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime


def get_page_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Accept-Language': 'en-US'}
    page = requests.get(url, headers=headers)
    print(page.status_code)
    return page.content


def check_item_in_stock_inet(page_html):
    soup = BeautifulSoup(page_html, 'html5lib')
    if soup.find("span", {"class": "in-stock stock-blob product-qty-blob"}):
        return 1


def check_item_in_stock_komplett(page_html):
    soup = BeautifulSoup(page_html, 'html5lib')
    if soup.find("div", {"class": "stockstatus"}):
        return 1


def check_item_in_stock_netonnet(page_html):
    soup = BeautifulSoup(page_html, 'html5lib')
    if soup.find("div", {"class": "stock-status"}):
        return 1


# special case, uses webhallen's own server search API
def check_item_in_stock_webhallen():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Accept-Language': 'en-US'}
    BASE = "https://www.webhallen.com/api/product/"
    product_ids = {"320479", "300815"}
    for product_id in product_ids:
        req = requests.get(BASE + product_id, headers=headers)
        response_data = req.json()
        product = response_data["product"]
        in_stock = False
        in_stock = product["stock"]["web"] > 0
        if in_stock == True:
            print(product["name"])
            print(product["price"]["price"])
            return 1


def check_inventory():
    urls = {"https://www.inet.se/produkt/6609862/sony-playstation-5-digital-edition", "https://www.inet.se/produkt/6609649/sony-playstation-5", "https://www.komplett.se/product/1111557/gaming/playstation/playstation-5-ps5", "https://www.komplett.se/product/1161553/gaming/playstation/playstation-5-digital-edition-ps5", "https://www.webhallen.com/se/product/346166-MSI-Optix-G251F-25-IPS-1080p-1ms-165Hz-DP-HDMI-HDR-G-Sync", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5/1012886.14413/", "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-digital-edition/1013477.14413/" }
    #testUrls = {"https://www.inet.se/produkt/5412819/d-link-e15-ax1500-mesh-range-extender",
            #"https://www.komplett.se/product/1161554/gaming/tillbehor-till-spelkonsoler/playstation-5-hd-camera",
           # "https://www.webhallen.com/se/product/346166-MSI-Optix-G251F-25-IPS-1080p-1ms-165Hz-DP-HDMI-HDR-G-Sync",
            #"https://www.netonnet.se/art/gaming/spel-och-konsol/xbox/xbox-konsol/microsoft-xbox-series-s/1012885.14412/"}
    for url in urls:
        page_html = get_page_html(url)

        if "inet" in url:
            if check_item_in_stock_inet(page_html):
                print("Item in inet stock 123")
            else:
                print("Item not in inet stock")

        elif "komplett" in url:
            if check_item_in_stock_komplett(page_html):
                print("item in komplett stock 123")
            else:
                print("item not in komplett stock")

        elif "webhallen" in url:
            if check_item_in_stock_webhallen():
                print("Item in webbhallen stock 123")
            else:
                print("Item not in webhallen stock")

        elif "netonnet" in url:
            if check_item_in_stock_netonnet(page_html):
                print("Item in netonnet stock 123")
            else:
                print("Item not in netonnet stock")


while (1):
    check_inventory()
    print("check done at: " + str(datetime.now()))
    time.sleep(55)
