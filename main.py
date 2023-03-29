
from bs4 import BeautifulSoup
import asyncio
import time
import aiohttp
from scraper import *
from selenium import webdriver
import xlwriter

async def get_driver():
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--headless")

## Add Options to Webdriver 
    driver = webdriver.Chrome(options=chrome_options)
    return driver



async def main():
    pages = [f"https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&page={number}" for number in range(1,10)]
    tasks=[asyncio.create_task(get_product_urls_from_main_page(page)) for page in pages]
    product_links=await asyncio.gather(*tasks)
    driver = await get_driver()
    tasks=[asyncio.create_task(get_full_product_page(driver,link)) for product_link in product_links for link in product_link ]
    SOUPS=await asyncio.gather(*tasks)
    writer = xlwriter.BasicInfoWriter()
    tasks=[asyncio.create_task(writer.write_basic_info(soup)) for soup in SOUPS]
    await asyncio.gather(*tasks)




t1=time.time()
r=asyncio.run(main())
print(product_links)
print(ALL_PRODUCT_NAME)

t2=time.time()
print(t2-t1)
    
        
        
