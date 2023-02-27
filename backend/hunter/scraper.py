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
        
    def init_website_tags(self, product_tag, product_filter, name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag,  url_filter,):
        tag_data = TagData()
        tag_data.productTag = product_tag
        tag_data.productFilter = product_filter
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
        url = 'https://www.komplett.se/category/12769/gaming/playstation'
        # Check if website already exists in the database
        website = Website.objects.filter(url=url).first()
        if website:
            return website
        # Define website info
        website = Website()
        website.name = 'Komplett'
        website.url = url
        website.save()

        # Define the required HTML tags
        product_tag = 'div'
        product_filter = {'class': 'product-list-item'}
        name_tag = 'div'
        name_filter = {'class': 'text-content'}
        price_tag = 'span' 
        price_filter = {'class': 'product-price-now'}
        availability_tag = 'i'
        availability_filter = {"class": "icon icon-sm stockstatus-instock"}
        url_tag = 'a'
        url_filter = {"class": "product-link"}

        # Initialize the Tag data object
        tag_data = self.init_website_tags(product_tag, product_filter, name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag, url_filter)
        tag_data.relatedWebsite = website
        tag_data.save()
        website.relatedTagData = tag_data
        website.save()
        return website

    def create_scraping_object_inet(self):
        url = 'https://www.inet.se/kategori/751/konsoler'
        # Check if website already exists in the database
        website = Website.objects.filter(url=url).first()
        if website:
            return website
        # Define website info
        website = Website()
        website.name = 'Inet'
        website.url = url
        website.save()

        # Define the required HTML tags
        product_tag = 'li'
        product_filter = {'class': 'l1qhmxkx'}
        name_tag = 'h4'
        name_filter = {'class': 'h1nslqy4'}
        price_tag = 'span' 
        price_filter = {'class': 'bp5wbcj'}
        availability_tag = 'span'
        availability_filter = {'class': 's1ys0gx5 s14li1pv'}
        url_tag = 'a'
        url_filter = {"class": "a19jwzoe"}

        # Initialize the Tag data object
        tag_data = self.init_website_tags(product_tag, product_filter, name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag, url_filter)
        tag_data.relatedWebsite = website
        tag_data.save()
        website.relatedTagData = tag_data
        website.save()
        return website

    def create_scraping_object_netonnet(self):
        url = 'https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol'
        # Check if website already exists in the database
        website = Website.objects.filter(url=url).first()
        if website:
            return website
        # Define website info
        website = Website()
        website.name = 'Netonnet'
        website.url = url
        website.save()

        # Define the required HTML tags
        product_tag = 'div'
        product_filter = {'class': 'cProductItem col-xs-12 col-sm-4 col-md-6 col-lg-4 product'}
        name_tag = 'div'
        name_filter = {'class': 'subTitle small productList'}
        price_tag = 'span' 
        price_filter = {'class': 'price'}
        availability_tag = 'i'
        availability_filter = {'class': 'svg small success check'}
        url_tag = 'div'
        url_filter = {"class": "leftContent"}

        # Initialize the Tag data object
        tag_data = self.init_website_tags(product_tag, product_filter, name_tag, name_filter, price_tag, price_filter, availability_tag, availability_filter, url_tag, url_filter)
        tag_data.relatedWebsite = website
        tag_data.save()
        website.relatedTagData = tag_data
        website.save()
        return website

    def scrape_website(self, website):
        # Make a request to the website URL
        response = requests.get(website.url, headers=self.headers)
        response.raise_for_status()

        # Parse the HTML content with Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product information using the specified HTML tags
        product_divs = soup.find_all(website.relatedTagData.productTag, website.relatedTagData.productFilter)
        created = False
        if not product_divs:
            raise ValueError('No products found on website')
        for product_div in product_divs:
            product_name_tag = product_div.find(website.relatedTagData.nameTag, website.relatedTagData.nameFilter)
            if product_name_tag is None:
                continue
            product_name = product_name_tag.text.strip()
            if product_name == "":
                continue

            product_price_tag = product_div.find(website.relatedTagData.priceTag, website.relatedTagData.priceFilter)
            if product_price_tag is None:
                continue
            price_text = product_price_tag.text.strip()
            product_price = ''.join(filter(str.isdigit, price_text))

            product_availability = False
            availability_tag = product_div.find(website.relatedTagData.availabilityTag, website.relatedTagData.availabilityFilter)
            if availability_tag is not None:
                product_availability = True

            product_url_tag = product_div.find(website.relatedTagData.urlTag, website.relatedTagData.urlFilter)
            if product_url_tag is None or 'href' not in product_url_tag.attrs:
                continue
            product_url = product_url_tag['href']

            # Create a new Product object related to the given Website object
            product = Product()
            product.name = product_name
            product.availability = product_availability
            product.url = product_url
            product.price = product_price
            product.website = website
            product.dateCreated = timezone.now()
            product.dateUpdated = timezone.now()
            # Check if the product already exists in the database
            try:
                existing_product = Product.objects.get(name=product_name, website=website)
            except Product.DoesNotExist:
                existing_product = None

            if not existing_product:
                # Create a new Product object related to the given Website object
                created = True
                product.save()
            else:
                created = False
                # Update the existing product object
                existing_product.availability = product_availability
                existing_product.url = product_url
                existing_product.price = product_price
                existing_product.dateUpdated = timezone.now()
                existing_product.save()

        return created

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
    
    def run_scraper(self):
        website1 = self.create_scraping_object_komplett()
        website2 = self.create_scraping_object_inet()

        products_added_or_updated = self.scrape_website(website1)
        products_added_or_updated = self.scrape_website(website2)

        return products_added_or_updated