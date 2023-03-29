async def get_tale_of_size(soup):
    try:
        table = soup.find('table', {'class': 'sizeChartTable'})
        headers = table.find_all('th', {'class': 'sizeChartTHeaderCell'})
        rows = soup.find_all('tr','sizeChartTRow')
        return table,headers,rows
    except:
        return (None,None,None)

async def get_code(soup):
        span = soup.find('span', 'test-itemComment-article')
        return span.text