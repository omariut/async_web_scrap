from bs4 import BeautifulSoup
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

async def get_web_page_content(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')
            return soup


async def get_product_urls_from_main_page(url):

    element='a'
    class_name='image_link'
    soup=await get_web_page_content(url)
    product_links=[]
    image_link_objects= soup.find_all(element, class_name)

    for link_object in image_link_objects:
        url="https://shop.adidas.jp" + link_object["href"]
        if url not in product_links:
            product_links.append(url)
    return product_links

async def get_full_product_page(driver,url):
    driver.get(url)
    time.sleep(1)
    elem = driver.find_element(By.TAG_NAME, "body")
    while True:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
            break

    # Capture page source after all content is loaded
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    return soup
    
