import requests
from bs4 import BeautifulSoup
import asyncio
import time
product_links = []

def get_web_page(url):
   
    return requests.get(url)


def get_links(page_number):
    start_url = f"https://shop.adidas.jp/item/?page={page_number}"
    web_page= get_web_page(start_url)
    
    soup = BeautifulSoup(web_page.content, 'html.parser')
    for link in soup.find_all('a','image_link'):
        if link["href"] not in product_links:
            product_links.append("https://shop.adidas.jp" + link["href"])

def crawl_pages():
    for page_number in range(1,10):
        get_links(page_number)

t1=time.time()
crawl_pages()
t2=time.time()
print(t2-t1)