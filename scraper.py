from bs4 import BeautifulSoup
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlsxwriter
import time
ALL_PRODUCT_NAME=[]
SOUPS=[]
product_links=[]

async def get_web_page_content(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')
            return soup

async def get_html_object(soup,element,class_name,many=False):
    if many==True:
        return soup.find_all(element,class_name)
    return soup.find(element,class_name)

async def get_product_urls_from_main_page(url):

    element='a'
    class_name='image_link'
    soup=await get_web_page_content(url)
    product_links=[]
    image_link_objects=await get_html_object(soup, element, class_name,many=True)

    for link_object in image_link_objects:
        url="https://shop.adidas.jp" + link_object["href"]
        if url not in product_links:
            product_links.append(url)
    return product_links

async def get_full_product_page(driver,url):
    driver.get(url)
    time.sleep(5)
    elem = driver.find_element(By.TAG_NAME, "body")
    while True:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
            break

    # Capture page source after all content is loaded
    html = driver.page_source

    # Close Selenium driver

    # Parse HTML with bs4
    soup = BeautifulSoup(html, "html.parser")
    return soup
    

async def get_code(soup):
    span=  soup.find('span','test-itemComment-article')
    return span.text

async def get_product_name(soup):
    name_object= await get_html_object(soup, 'h1', 'itemTitle test-itemTitle')
    product_name= name_object.text
    return product_name

async def get_image_url(soup):
    image_object=await get_html_object(soup, 'img', 'main_image')
    return image_object["src"]

async def get_tale_of_size(soup):
    try:
        table = soup.find('table', {'class': 'sizeChartTable'})
        headers = table.find_all('th', {'class': 'sizeChartTHeaderCell'})
        rows = soup.find_all('tr','sizeChartTRow')
        return table,headers,rows
    except:
        return (None,None,None)
        
        










    # Close the workbook
    workbook.close()
    return headers
    

async def get_category_name(soup):
    span= await get_html_object(soup, 'span', 'categoryName test-categoryName')
    return span.text

async def get_pricing(soup):
    span= await get_html_object(soup, 'span', 'price-value test-price-value')
    return span.text

async def get_sizes(soup):
    buttons= await get_html_object(soup, 'button', 'sizeSelectorListItemButton',many=True)
    return str([item.text for item in buttons])

async def get_coordinated_product_names(soup):
    names = await get_html_object(soup, 'div', 'articleBadgeText test-text test-badge-label',many=True)
    return str([item.text for item in names])

async def get_coordinated_product_prices(soup):
    price_divs= await get_html_object(soup, 'div', 'coordinate_price',many=True)
    price_spans=[item.find('span') for item in price_divs]
    return str([item.text for item in price_spans])

async def get_description_title(soup):
    h4 = await get_html_object(soup, 'h4', 'heading itemFeature test-commentItem-subheading')
    return h4.text

async def get_general_description(soup):
    div = await get_html_object(soup, 'div', 'commentItem-mainText test-commentItem-mainText')
    return div.text

async def get_itemized_general_description(soup):
    ul = await get_html_object(soup, 'ul', 'articleFeatures description_part css-1lxspbu')
    items=ul.find_all('li')
    return str([item.text for item in items])

async def get_all_kws(soup):
    links = await get_html_object(soup, 'a', 'css-1ka7r5v',many=True)
    return str([item.text for item in links])

async def get_ratings(soup):
    img = await get_html_object(soup, 'img', 'BVImgOrSprite')
    return img["title"]

async def get_number_of_reviews(soup):
    span = await get_html_object(soup, 'span', 'BVRRNumber BVRRBuyAgainTotal')
    return span.text

async def get_sense_of_fit_rating(soup):
    soup=await get_html_object(soup, 'div', 'BVRRRatingFit')
    img=soup.find('img',"BVImgOrSprite")
    return img["title"]

async def get_quality_rating(soup):
    soup=await get_html_object(soup, 'div', 'BVRRRatingQuality')
    img=soup.find('img',"BVImgOrSprite")
    return img["title"]


async def get_comfort_rating(soup):
    soup=await get_html_object(soup, 'div', 'BVRRRatingComfort')
    img=soup.find('img',"BVImgOrSprite")
    return img["title"]

    


    
#review 
async def get_review_rating(review_soup):
    div = await get_html_object(review_soup, 'div','BVRRRatingNormalImage')
    rating=div.find("img")["title"]
    return rating

async def get_review_title(review_soup):
    span = await get_html_object(review_soup, 'span' , 'BVRRValue BVRRReviewTitle' )
    return span.text

async def get_review_text(review_soup):
    span = await get_html_object(review_soup, 'span', 'BVRRReviewText')
    return span.text

async def get_recommendation(review_soup):
    span=await get_html_object(review_soup, 'span', 'BVRRValue BVRRRecommended')
    return span.text

async def get_reviewer_name(review_soup):
    span=await get_html_object(review_soup, 'span', 'BVRRNickname')
    return span.text

async def get_review_data(review_soup):
    rating = await get_review_rating(review_soup)
    title = await get_review_title(review_soup)
    text = await get_review_text(review_soup)
    recommendation = await get_recommendation(review_soup)
    name = await get_reviewer_name(review_soup)
    return name,rating,title,text,recommendation


async def get_all_review_soups(soup):
    return await get_html_object(soup, 'div', 'BVRRReviewDisplayStyle5', many=True) 


async def get_all_review_data(soup):
    review_soups = await get_all_review_soups(soup)
    print(len(review_soups))
    review_data = []
    for soup in review_soups:
        data = await get_review_data(soup)
        review_data.append(data)
    return review_data
