from bs4 import BeautifulSoup
import aiohttp
import asyncio
async def get_size():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://shop.adidas.jp/products/HQ6786/') as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')
            buttons=soup.find_all('button','sizeSelectorListItemButton')
            sizes =[i.text for i in buttons]

    return sizes


sizes = asyncio.run(get_size())
print(sizes)