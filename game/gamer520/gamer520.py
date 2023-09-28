# 导入 requests 包
import requests
from lxml import etree
import pandas
import time
from hyper.contrib import HTTP20Adapter


# hot_url = "https://www.gamer520.com/pcgame?order=hot"
# comment_url = "https://www.gamer520.com/pcgame?order=comment_count"

# hot_page_num_url = "https://www.gamer520.com/pcgame/page/2?order=hot"


def getHotUrl(page, type):
    # page 页数
    # type 1 表示 hot， 2 表示 comment_count
    if page == 1:
        if type == 1:
            return "https://www.gamer520.com/pcgame?order=hot"
        else:
            return "https://www.gamer520.com/pcgame?order=comment_count"
    else:
        if type == 1:
            return "https://www.gamer520.com/pcgame/page/{}?order=hot".format(page)
        else:
            return "https://www.gamer520.com/pcgame/page/{}?order=comment_count".format(page)

num = 0
page_count = 427
all_articles = []

def send_request(type):
    global num
    num = num + 1
    request_url = getHotUrl(num, type)
    print("send request -> " + request_url)
    request_headers = {':authority': 'www.gamer520.com', 
                       ':method': 'GET', 
                       ':path': request_url.replace("https://www.gamer520.com", ""), 
                       ':scheme': 'https', 
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
                       'Accept-Encoding': 'gzip, deflate, br', 
                       'Accept-Language': 'zh-CN,zh;q=0.9', 
                       'Cache-Control': 'max-age=0', 
                       'Cookie': 'PHPSESSID=v8c6aagqo9fjcrm52ga5ih9afb; cf_clearance=Cdj0SwB_4kByKBif62AK0P1B0nYaHDlP4e7.xylU3_U-1695910198-0-1-5801d1a0.88508328.f008e40-0.2.1695910198; _ga=GA1.1.1927702210.1695910202; cao_notice_cookie=1; _ga_MB6TSGCTV9=GS1.1.1695910202.1.1.1695911582.0.0.0', 
                       'Referer': request_url, 
                       'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"', 
                       'Sec-Ch-Ua-Mobile': '?0', 
                       'Sec-Ch-Ua-Platform': '"Windows"', 
                       'Sec-Fetch-Dest': 'document', 
                       'Sec-Fetch-Mode': 'navigate', 
                       'Sec-Fetch-Site': 'same-origin', 
                       'Sec-Fetch-User': '?1', 
                       'Upgrade-Insecure-Requests': '1', 
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    
    session = requests.session()
    session.mount(prefix='https://', adapter = HTTP20Adapter())
    response = session.get(request_url, headers=request_headers)
    # print(response.text)
    parse_response(response.text)

def parse_response(response):
    html = etree.HTML(response)
    h2_list = html.xpath("//h2[@class='entry-title']")
    article_list = []

    for h2 in h2_list:
        title = h2.xpath("./a[1]/text()")[0]
        print(title)
        article_list.append(title)
        all_articles.append(Article(title))


def get_comment(article):
    return int(article.comment.replace(",", ""))

def print_articles(articles):
    articles.sort(key = get_comment)
    for article in articles:
        print(article.title + ":" + str(article.comment))

def output_excel(articles):
    articles.sort(key = get_comment, reverse=True)
    data = []
    for article in articles:
        data.append(article.toList())
        # print(article.title + ":" + str(article.comment))
    pd = pandas.DataFrame(data=data, columns=["游戏名","评论数"])
    pd.to_excel('game.xlsx')

class Article:
    def __init__(self, title):
      self.title = title

    def toList(self):
       return [self.title]
   

if __name__=="__main__":
    # for i in range(1, page_count + 1):
    send_request(1)
        # time.sleep(3)
    # output_excel(articles=all_articles)
    # print("6,779".replace(",", ""))