from bs4 import BeautifulSoup
import time
import requests
from django.utils import timezone
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
        
    def init_website_tags(self, name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag,  url_filter,):
        tag_data = TagData()
        tag_data.nameTag = name_tag
        tag_data.nameFilter = name_filter
        tag_data.priceTag = price_tag
        tag_data.priceFilter = price_filter
        tag_data.availabilityTag = availability_tag
        tag_data.availabilityFilter = availability_filter
        tag_data.urlTag = url_tag
        tag_data.urlFilter = url_filter
        return tag_data

    def create_scraping_object_komplett(self):
        # Define website info
        website = Website()
        website.name = 'Komplett'
        website.url = 'https://www.komplett.se/category/12769/gaming/playstation'
        website.save()

        # Define the required HTML tags
        name_tag = 'div'
        name_filter = {'class': 'text-content'}
        price_tag = 'span' 
        price_filter = {'class': 'product-price-now'}
        availability_tag = "div"
        availability_filter = {"class": "stockstatus"}
        url_tag = 'a'
        url_filter = {"class": "product-link"}

        # Initialize the Tag data object
        tag_data = self.init_website_tags(name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag, url_filter)
        tag_data.relatedWebsite = website
        tag_data.save()
        website.relatedTagData = tag_data
        website.save()
        return website

    def scrape_website(self, website):
        # Make a request to the website URL
        response = requests.get(website.url, headers=self.headers)

        # Parse the HTML content with Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product information using the specified HTML tags
        product_name = soup.find(website.relatedTagData.nameTag, website.relatedTagData.nameFilter)
        product_price = soup.find(website.relatedTagData.priceTag, website.relatedTagData.priceFilter)
        product_availability = soup.find(website.relatedTagData.availabilityTag, website.relatedTagData.availabilityFilter)
        product_url = soup.find(website.relatedTagData.urlTag, website.relatedTagData.urlFilter)['href']

        print(product_name)
        print(product_price)
        print(product_availability)
        print(product_url)

        # Create a new Product object related to the given Website object
        product = Product.objects.create(
            name=product_name,
            availability=(product_availability == 'In Stock'),
            url=product_url,
            price=product_price,
            website=website,
            dateCreated=timezone.now(),
            dateUpdated=timezone.now(),
        )
        # Save the new Product object to the database
        product.save()
        return product
        
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
        div = "div"
        stock_filter = {"class": "stockstatus"}
        if soup.find(div, stock_filter):
            in_stock = True
        namediv = 'span'
        namefilter = {'data-bind': 'text: webtext1'}
        name = soup.find(namediv, namefilter).text
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
        website = self.create_scraping_object_komplett()
        self.scrape_website(website)
        return 1