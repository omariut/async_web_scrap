
from bs4 import BeautifulSoup
import asyncio
import time
import aiohttp

r = []

async def scrape(url):
    print('hello')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')
            product_links = soup.find_all('a','image_link')
            for link in product_links:
                if link["href"] not in r:
                    r.append("https://shop.adidas.jp" + link["href"])

async def get_page(number):
    return f"https://shop.adidas.jp/item/?page={number}" 

async def get_web_page(page):
    print('hello')
    return requests.get(page)

async def get_soup(webpage):
    return BeautifulSoup(web_page.content, 'html.parser')

async def get_link(soup):
    r=[]
    for link in soup.find_all('a','image_link'):
        if link["href"] not in product_links:
            r.append("https://shop.adidas.jp" + link["href"])

    

async def get_links(page_number):
    pages = await get_all_pages(page_number)
    webpages=asyncio.gather(get_web_page(page) for page in pages)
    soups = asyncio.gather(get_soup(webpage) for webpage in webpages)
    links=asyncio.gather(get_link(soup) for soup in soups)
    print(links)

async def main():
    pages = [f"https://shop.adidas.jp/item/?page={number}" for number in range(1,11)]
    tasks=[asyncio.create_task(scrape(page)) for page in pages]
    await asyncio.gather(*tasks)


t1=time.time()
asyncio.run(main())
print(r)
t2=time.time()
print(t2-t1)
    
        
        
