import aiohttp
from bs4 import BeautifulSoup


class Review:
    def __init__(self, soup):
        self.soup = soup

    async def get_code(self):
        span = self.soup.find('span', 'test-itemComment-article')
        return span.text

    async def get_ratings(self):
        img = self.soup.find('img', 'BVImgOrSprite')
        return img["title"]

    async def get_number_of_reviews(self):
        span = self.soup.find('span', 'BVRRNumber BVRRBuyAgainTotal')
        return span.text

    async def get_sense_of_fit_rating(self):
        img = self.soup.find('img', 'BVImgOrSprite')
        return img["title"]

    async def get_quality_rating(self):
        img = self.soup.find('img', 'BVImgOrSprite')
        return img["title"]

    async def get_comfort_rating(self):
        img = self.soup.find('img', 'BVImgOrSprite')
        return img["title"]

    async def get_review_rating(self):
        div = self.soup.find('div', 'BVRRRatingNormalImage')
        rating = div.find("img")["title"]
        return rating

    async def get_review_title(self):
        span = self.soup.find('span' , 'BVRRValue BVRRReviewTitle' )
        return span.text

    async def get_review_text(self):
        span = self.soup.find('span', 'BVRRReviewText')
        return span.text

    async def get_recommendation(self):
        span = self.soup.find('span', 'BVRRValue BVRRRecommended')
        return span.text

    async def get_reviewer_name(self):
        span = self.soup.find('span', 'BVRRNickname')
        return span.text

    async def get_review_data(self):
        rating = await self.get_review_rating()
        title = await self.get_review_title()
        text = await self.get_review_text()
        recommendation = await self.get_recommendation()
        name = await self.get_reviewer_name()
        return name, rating, title, text, recommendation

    async def get_all_user_review_data(self):
        review_data = []
        review_soups = self.soup.find_all('div', 'BVRRReviewDisplayStyle5')
        for review_soup in review_soups:
            review = Review(review_soup)
            data = await review.get_review_data()
            review_data.append(data)
        return review_data


    async def get_general_review_data(self):
        overall_rating = await self.get_ratings()
        quality_rating = await self.get_quality_rating()
        total_reviews = await self.get_number_of_reviews()
        sense_of_fit_rating = await self.get_sense_of_fit_rating()
        comfort_rating = await self.get_comfort_rating()

        return overall_rating, quality_rating, total_reviews, sense_of_fit_rating, comfort_rating





