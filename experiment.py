from scraper import *
import asyncio
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
    pages = [f"https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&page={number}" for number in range(1,20)]
    tasks=[asyncio.create_task(get_product_urls_from_main_page(page)) for page in pages]
    product_links=await asyncio.gather(*tasks)
    driver = await get_driver()
    tasks=[asyncio.create_task(get_full_product_page(driver,link)) for product_link in product_links for link in product_link ]
    SOUPS=await asyncio.gather(*tasks)

    basic_writer = xlwriter.BasicInfoWriter()
    tasks=[asyncio.create_task(basic_writer.write_basic_info(soup)) for soup in SOUPS]
    await asyncio.gather(*tasks)
    basic_writer.workbook.close()

    tale_size_writer=xlwriter.TaleOfSizeWriter()
    tasks=[asyncio.create_task(tale_size_writer.write_tale_of_size(soup)) for soup in SOUPS]
    await asyncio.gather(*tasks)
    tale_size_writer.workbook.close()
   

asyncio.run(main())




