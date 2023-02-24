from django.test import TestCase
import unittest
from unittest.mock import patch, MagicMock
from .scraper import Scraper
import requests

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Accept-Language': 'en-US'}

    def test_check_item_in_stock_inet(self):
        page = requests.get("https://www.inet.se/produkt/6335950/microsoft-xbox-series-x", headers=self.headers)
        page_html = page.content
        expected_data = {
            'name': 'Microsoft Xbox Series X',
            'website': 'Inet',
            'availability': True,
            'url': 'https://www.inet.se/produkt/6335950/microsoft-xbox-series-x',
            'price': '6195',
        }

        data = self.scraper.check_item_in_stock_inet(page_html)
        self.assertEqual(data, expected_data)

    def test_check_item_in_stock_komplett(self):
        page = requests.get("https://www.komplett.se/product/1220599/gaming/playstation/playstation-5-och-god-of-war-ragnarok", headers=self.headers)
        page_html = page.content
        expected_data = {
            'name': 'PlayStation 5 och God of War Ragnarök',
            'website': 'Komplett',
            'availability': True,
            'url': 'https://www.komplett.se/product/1220599/gaming/playstation/playstation-5-och-god-of-war-ragnarok',
            'price': '7790',
        }

        data = self.scraper.check_item_in_stock_komplett(page_html)
        self.assertEqual(data, expected_data)

    def test_check_item_in_stock_netonnet(self):
        page = requests.get("https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-c-chassi/1027489.14413/", headers=self.headers)
        page_html = page.content
        expected_data = {
            'name': 'PlayStation 5',
            'website': 'Netonnet',
            'availability': True,
            'url': 'https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5-c-chassi/1027489.14413/',
            'price': 7290,
        }

        data = self.scraper.check_item_in_stock_netonnet(page_html)
        self.assertEqual(data, expected_data)

    def test_check_item_in_stock_webhallen(self):
        expected_data = {
            'name': 'Playstation 5 Konsol (PS5)',
            'website': 'Webhallen',
            'availability': True,
            'url': '',
            'price': 7290.0,
        }
        data = self.scraper.check_item_in_stock_webhallen()
        self.assertEqual(data, expected_data)