import xlsxwriter
import asyncio
import product_scraper
import review_scraper
import tale_of_size_scraper

class ExcelWriter:
    def __init__(self,file_name):
        self.workbook = xlsxwriter.Workbook(file_name)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.row=0
        self.worksheet.column=0

class BasicInfoWriter(ExcelWriter):
    
    def __init__(self):
        super().__init__('basic_info.xlsx')
        worksheet = self.worksheet
        worksheet.write(1,1,'code')
        worksheet.write(1,2,'name')
        worksheet.write(1,3,'category')
        worksheet.write(1,4,'image_url')
        worksheet.write(1,5,'kws')
        worksheet.write(1,6,'price')
        worksheet.write(1,7,'sizes')
        worksheet.write(1,8,'cord_product')
        worksheet.write(1,9,'cord_product_price')
        worksheet.write(1,10,'descraperion_title')
        worksheet.write(1,11,'descraperion')
        self.row=2
    
    async def get_basic_info(self,soup):
        scraper = product_scraper.Product(soup)
        self.code =await scraper.get_code()
        self.name=await scraper.get_product_name()
        self.category=await scraper.get_category_name()
        self.image_url=await scraper.get_image_url()
        self.kws=await scraper.get_all_kws()
        self.price = await scraper.get_pricing()
        self.sizes=await scraper.get_sizes()
        self.cord_product=await scraper.get_coordinated_product_names()
        self.cord_product_price=await scraper.get_coordinated_product_prices()
        self.descraperion_title=await scraper.get_description_title()
        self.descraperion=await scraper.get_general_description()


    async def write_basic_info(self,soup):
        try:
            await self.get_basic_info(soup)
            worksheet = self.worksheet
            worksheet.write(self.row,1,self.code)
            worksheet.write(self.row,2,self.name)
            worksheet.write(self.row,3,self.category)
            worksheet.write(self.row,4,self.image_url)
            worksheet.write(self.row,5,self.kws)
            worksheet.write(self.row,6,self.price)
            worksheet.write(self.row,7,self.sizes)
            worksheet.write(self.row,8,self.cord_product)
            worksheet.write(self.row,9,self.cord_product_price)
            worksheet.write(self.row,10,self.descraperion_title)
            worksheet.write(self.row,11,self.descraperion)
            self.row+=1
        except:
            pass
       
    

class TaleOfSizeWriter(ExcelWriter):
    def __init__(self):
        super().__init__('tale_size_info.xlsx')
        merge_format = self.workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            })
        self.worksheet.merge_range('B1:K1', 'Table', merge_format)
        self.worksheet.write(0, 0,'code')
        self.worksheet.row=1


    async def write_tale_of_size(self,soup):
        try:
            scraper = tale_of_size_scraper
            code = await scraper.get_code(soup)
            table,headers,rows = await scraper.get_tale_of_size(soup)
            if not table:
                return 
            worksheet=self.worksheet
            row=worksheet.row
            col=0
            worksheet.write(row, col,code)
            col=1
            for header in headers:
                worksheet.write(row,col,header.text)
                row+=1
            
            last_row=row
            row=worksheet.row
            col=2
                
            for item in rows:
                cells = item.find_all('td','sizeChartTCell')
                if cells:
                    for cell in cells:
                        
                        worksheet.write(row,col,cell.text)
                        col+=1
                    col=2
                    row+=1
            worksheet.row=last_row+2
        except:
            pass

class ReviewDataWriter(ExcelWriter):
    def __init__(self):
        super().__init__('review_info.xlsx')
        self.row=0
        self.col=0
        worksheet = self.worksheet
        worksheet.write(0,0,"code")
        worksheet.write(0,1,"overall_rating")
        worksheet.write(0,2,"quality_rating")
        worksheet.write(0,3,"total_reviews")
        worksheet.write(0,4,"sense_of_fit_rating")
        worksheet.write(0,5,"comfort_rating")
        worksheet.write(0,6,'name')
        worksheet.write(0,7,'rating')
        worksheet.write(0,8,'title')
        worksheet.write(0,9,'text')
        worksheet.write(0,10,'recommendation')
        self.row+=1
    
    
    async def write_review_data(self,soup):
        try:
            worksheet = self.worksheet
            scraper = review_scraper.Review(soup)
            all_review_data = await scraper.get_all_user_review_data()
            code = await scraper.get_code()
            


        

            overall_rating,quality_rating,total_reviews,sense_of_fit_rating,comfort_rating= await scraper.get_general_review_data()

            worksheet.write(self.row,0, code)
            worksheet.write(self.row,1,overall_rating)
            worksheet.write(self.row,2,quality_rating)
            worksheet.write(self.row,3,total_reviews)
            worksheet.write(self.row,4,sense_of_fit_rating)
            worksheet.write(self.row,5,comfort_rating)
        

            for data in all_review_data:
                name=data[0]
                rating=data[1]
                title=data[2]
                text=data[3]
                recommendation=data[4]

                worksheet.write(self.row,6,name)
                worksheet.write(self.row,7,rating)
                worksheet.write(self.row,8,title)
                worksheet.write(self.row,9,text)
                worksheet.write(self.row,10,recommendation)
                self.row+=1
            self.row+=1
        except:
            pass
    


