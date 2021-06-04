import requests
import pymongo  # 导入pymongo模块
import time
from bs4 import BeautifulSoup
import pandas as pd

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)

# 选择数据库
# db = client.admin
# 验证用户名
# db.authenticate("mongo", "swf5648413300")
# 切换库
col = client.JS_database.JS_string

# url请求文件头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.108 Safari/537.36'}
Cookie = {
    'Cookie': '__cfduid=d131a4f711404fc25b08d85c8d43514261616057698; '
              '__guid=260276875.3777610115178723300.1616057700611.5947; _ga=GA1.2.516020428.1616057702; '
              '_gid=GA1.2.1347638989.1616057702; '
              'trc_cookie_storage=taboola%2520global%253Auser-id%3Dc0c43b1f-5a6a-45ca-a5b4-6b5f8c47d79f-tuct74c9ae5; '
              'monitor_count=6'}
url_1 = 'https://www.w3resource.com/javascript-exercises/javascript-string-exercise-'
url_2 = '.php'
url_site = 'https://www.w3resource.com/assets/level_display.php'

# print(Get_difficulty.text)
# col.insert_one({'difficulty': Get_difficulty.text})
i = 1
while True:
    url = url_1 + str(i) + url_2
    param = {
        'page': url
    }
    try:
        # 主界面
        html_solution = requests.get(url, headers=header, cookies=Cookie)
        # 难度
        difficulty = requests.post(url_site, data=param, headers=header).text.split('-')[1]
        # BeautifulSoup解析网址
        soup = BeautifulSoup(html_solution.content, 'html.parser')
        # 题目
        title = soup.find_all('h1', attrs={'class': 'heading'})
        # html代码
        code_html = soup.find_all('code', attrs={'class': 'language-html'})
        # js代码
        code_js = soup.find_all('code', attrs={'class': 'language-js'})
        if len(title) == 0:
            break
        for jj in range(len(title)):
            data1 = [(i, title[jj].string, code_html[jj].string, code_js[jj].string, difficulty)]
            data2 = pd.DataFrame(data1)
            col.insert_one({'id': i, 'title': title[jj].string, 'html_answer': code_html[jj].string, 'difficulty': difficulty})
    except:
        print("Wrong!")
    print('page ' + str(i) + ' is done')
    i = i + 1
    time.sleep(2)
