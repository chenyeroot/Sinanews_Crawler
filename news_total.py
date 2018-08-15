import requests
from bs4 import BeautifulSoup 
import pandas as pd

res = requests.get('http://news.sina.com.cn/o/2018-07-12/doc-ihfefkqr0818002.shtml')
res.encoding = 'utf-8'
print(res.text)

soup = BeautifulSoup(res.text,'html.parser')

#把取得评论数的代码封装起来
def getCommentCount(newsurl):
    commentsurl = 'http://comment5.news.sina.com.cn/page/info?version=1&\format=json&channel=gn&newsid=comos-{}'
    m = re.search('doc-i(.*).shtml',newsurl)
    newsid = m.group(1)
    comments = requests.get(commentsurl.format(newsid))
    jd = json.loads(comments.text)
    return jd['result']['count']['show']

#完成内文信息抽取函式
def getNewsDetail(newsurl):
    result={}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['comments'] = getCommentCount(newsurl)    
    result['source'] = soup.select('.source')[0].text
    result['datetime'] = soup.select('.date')[0].text
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：')
    result['title'] = soup.select('.main-title')[0].text
    return result
    
#建立剖析清单链接函式
def parseListLinks(url):
    newsdtails=[]
    res = requests.get(url)
    jd = json.loads(res.text.lstrip("  newsloadercallback(").rstrip(');'))
    for ent in jd['result']['data']:
        newsdtails.append(getNewsDetail(ent['url']))
    return newsdtails
  
#使用for 循环产生多页链接
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1531753642192'
news_total=[]
for i in range(1,10):
    newsurls = url.format(i)
    newsary = parseListLinks(newsurls)
    news_total.extend(newsary)#注意append和extend的区别
  
 #转化成df


news_total = pd.DataFrame(news_total)
news_total.head()

#写入excel文件
news_total.to_excel(".../news.xlsx")
