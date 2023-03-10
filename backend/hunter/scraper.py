from bs4 import BeautifulSoup
import time
import requests
import json
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
    
    def run_scraper(self):
        #gets all website objects from db, scraping each one for new product data
        websites = Website.objects.all()
        for website in websites:
            products_added_or_updated = self.scrape_website(website)
        return products_added_or_updated