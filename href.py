import requests
from bs4 import BeautifulSoup 
res = requests.get('https://movie.douban.com/top250')
res.encoding = 'utf-8'
print(res.text)

soup = BeautifulSoup(res.text,'html.parser')

#获取时间、标题，新闻链接
for news in soup.select('.news-item'):
    if len(news.select('h2'))>0:
        head = news.select('a')[0].text
        href = news.select('a')[0]['href']
        time = news.select('.time')[0].text
        print(time,head,href)
