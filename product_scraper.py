from bs4 import BeautifulSoup
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlsxwriter
import time

class Base:
    def __init__(self, soup):
        self.soup = soup
    
    async def get_code(self):
        raise NotImplementedError
    
    async def get_product_name(self):
        raise NotImplementedError
    
    async def get_image_url(self):
        raise NotImplementedError
    
    async def get_category_name(self):
        raise NotImplementedError
    
    async def get_pricing(self):
        raise NotImplementedError
    
    async def get_sizes(self):
        raise NotImplementedError
    
    async def get_coordinated_product_names(self):
        raise NotImplementedError
    
    async def get_coordinated_product_prices(self):
        raise NotImplementedError
    
    async def get_description_title(self):
        raise NotImplementedError
    
    async def get_general_description(self):
        raise NotImplementedError
    
    async def get_itemized_general_description(self):
        raise NotImplementedError
    
    async def get_all_kws(self):
        raise NotImplementedError

class Product(Base):
    def __init__(self, soup):
        super().__init__(soup)
    
    async def get_code(self):
        span = self.soup.find('span', 'test-itemComment-article')
        return span.text

    async def get_product_name(self):
        name_object = self.soup.find('h1', 'itemTitle test-itemTitle')
        product_name = name_object.text
        return product_name

    async def get_image_url(self):
        image_object = self.soup.find('img', 'main_image')
        return image_object['src']

    async def get_category_name(self):
        span = self.soup.find('span', 'categoryName test-categoryName')
        return span.text

    async def get_pricing(self):
        span = self.soup.find('span', 'price-value test-price-value')
        return span.text

    async def get_sizes(self):
        buttons = self.soup.find_all('button', 'sizeSelectorListItemButton')
        return str([item.text for item in buttons])

    async def get_coordinated_product_names(self):
        names = self.soup.find_all('div', 'articleBadgeText test-text test-badge-label')
        return str([item.text for item in names])

    async def get_coordinated_product_prices(self):
        price_divs = self.soup.find_all('div', 'coordinate_price')
        price_spans = [item.find('span') for item in price_divs]
        return str([item.text for item in price_spans])

    async def get_description_title(self):
        h4 = self.soup.find('h4', 'heading itemFeature test-commentItem-subheading')
        return h4.text

    async def get_general_description(self):
        div = self.soup.find('div', 'commentItem-mainText test-commentItem-mainText')
        return div.text

    async def get_itemized_general_description(self):
        ul = self.soup.find('ul', 'articleFeatures description_part css-1lxspbu')
        items = ul.find_all('li')
        return str([item.text for item in items])

    async def get_all_kws(self):
        links = self.soup.find_all('a', 'css-1ka7r5v')
        return str([item.text for item in links])
