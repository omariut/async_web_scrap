import xlwriter
import asyncio
import scraper
from selenium import webdriver
from sample_soup import soup
from bs4 import BeautifulSoup
soup=BeautifulSoup(soup,'html.parser')

async def get_driver():
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--headless")

## Add Options to Webdriver 
    driver = webdriver.Chrome(options=chrome_options)
    return driver

async def main():
    # pages = [f"https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&page={number}" for number in range(1,21)]
    # tasks=[asyncio.create_task(scraper.get_product_urls_from_main_page(page)) for page in pages]
    # product_links=await asyncio.gather(*tasks)
    # driver = await get_driver()
    # tasks=[asyncio.create_task(scraper.get_full_product_page(driver,link)) for product_link in product_links for link in product_link ]
    # SOUPS=await asyncio.gather(*tasks)

    review_writer = xlwriter.ReviewDataWriter()
    tasks=[asyncio.create_task(review_writer.write_review_data(soup)) for soup in [soup,soup,soup] ]#SOUPS]
    await asyncio.gather(*tasks)
    review_writer.workbook.close()

asyncio.run(main())