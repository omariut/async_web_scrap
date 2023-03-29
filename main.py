from page_scraper import *
import asyncio
from selenium import webdriver
import xlwriter

#for fast testing
from sample_soup import soup
from bs4 import BeautifulSoup
soup=BeautifulSoup(soup, 'html.parser')

async def get_driver():
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

async def main():

    #get all product links
    pages = [f"https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&page={number}" for number in range(1,20)]
    tasks=[asyncio.create_task(get_product_urls_from_main_page(page)) for page in pages]
    product_links=await asyncio.gather(*tasks)
    
    
    #gather all soups from all product page
    #product page needs driver to load as js simulation is not possible in aiohttp
    driver = await get_driver()
    tasks=[asyncio.create_task(get_full_product_page(driver,link)) for product_link in product_links for link in product_link ]
    
    SOUPS=await asyncio.gather(*tasks)

    #SOUPS = [soup,soup,soup,soup]


    #collect basic info
    basic_writer = xlwriter.BasicInfoWriter()
    tasks=[asyncio.create_task(basic_writer.write_basic_info(soup)) for soup in SOUPS]
    await asyncio.gather(*tasks)
    basic_writer.workbook.close()

    #collect tale of size
    tale_size_writer=xlwriter.TaleOfSizeWriter()
    tasks=[asyncio.create_task(tale_size_writer.write_tale_of_size(soup)) for soup in SOUPS]
    await asyncio.gather(*tasks)
    tale_size_writer.workbook.close()

    #collect review data
    review_writer = xlwriter.ReviewDataWriter()
    tasks=[asyncio.create_task(review_writer.write_review_data(soup)) for  soup in SOUPS ]#SOUPS]
    await asyncio.gather(*tasks)
    review_writer.workbook.close()
   

asyncio.run(main())




