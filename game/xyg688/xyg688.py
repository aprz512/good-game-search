# 导入 requests 包
import requests
from lxml import etree
import pandas
import time


base_url = "https://www.xyg688.com/page/"
num = 0
page_count = 364
all_articles = []

def send_request():
    global num
    num = num + 1
    request_url = base_url + str(num)
    print("send request -> " + request_url)
    request_headers = {
        'Authority': 'www.xyg688.com',
        'Method':'GET',
        'Path':'/page/18',
        'Scheme':'https',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Cookie':'quads_browser_width=2560; wp_xh_session_050f920e85de064de828e63d202b6615=f08bf57a2d09e95396f2c5572e39138c%7C%7C1689499581%7C%7C1689495981%7C%7C6c61dd8755a17af62fb0052bcff252e1; quads_browser_width=2560; wpdiscuz_hide_bubble_hint=1',
        'Referer':'https://www.xyg688.com/page/'+ str(num - 1),
        'Sec-Ch-Ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
    response = requests.get(request_url, headers=request_headers)
    # print(response.text)
    parse_response(response.text)

def parse_response(response):
    html = etree.HTML(response)
    grid_wrapper = html.xpath("//div[@id='grid-wrapper']")[0]
    article_list = grid_wrapper.xpath(".//article")
    # articles = []
    for article in article_list:
        commments = article.xpath("./div[1]/div[1]/a[2]/text()")
        if(not commments):
            return
        titles = article.xpath("./div[1]/div[2]/h2[1]/a[1]/text()")
        if(not titles):
            return
        all_articles.append(Article(commments[0], titles[0]))
    # print_articles(articles)

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
    def __init__(self, comment, title):
      self.comment = comment
      self.title = title

    def toList(self):
       return [self.title, self.comment]
   

if __name__=="__main__":
    for i in range(1, page_count + 1):
        send_request()
        # time.sleep(3)
    output_excel(articles=all_articles)
    # print("6,779".replace(",", ""))