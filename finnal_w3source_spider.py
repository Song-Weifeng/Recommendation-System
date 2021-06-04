import requests
from bs4 import BeautifulSoup
import re
import pymongo  # 导入pymongo模块
# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
# 切换库
col = client.JS_exercise.JS_sort
# url请求文件头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.108 Safari/537.36',
    'Connection': 'close'}
Cookie = {
    'Cookie': '__cfduid=d131a4f711404fc25b08d85c8d43514261616057698; '
              '__guid=260276875.3777610115178723300.1616057700611.5947; _ga=GA1.2.516020428.1616057702; '
              '_gid=GA1.2.1347638989.1616057702; '
              'trc_cookie_storage=taboola%2520global%253Auser-id%3Dc0c43b1f-5a6a-45ca-a5b4-6b5f8c47d79f-tuct74c9ae5; '
              'monitor_count=6'}
url_1 = 'https://www.w3resource.com/javascript-exercises/' \
        'searching-and-sorting-algorithm/searching-and-sorting-algorithm-exercise-'
url_2 = '.php'
url_site = 'https://www.w3resource.com/assets/level_display.php'
i = 1
while True:
    url = url_1 + str(i) + url_2
    # try:
    page = requests.get(url, headers=header, cookies=Cookie, timeout=50)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all('h1', attrs={'class': 'heading'})[0].string
    # html代码
    try:
        code_html = soup.find_all('code', attrs={'class': 'language-html'})[0].string
    except:
        code_html = soup.find_all('code', attrs={'class': 'language-markup'})[0].string
    # js代码
    try:
        code_js = soup.find_all('code', attrs={'class': 'language-javascript'})[0].string
    except:
        code_js = soup.find_all('code', attrs={'class': 'language-js'})[0].string
    information = soup.find_all('div', attrs={'class': 'mdl-cell mdl-card mdl-shadow--2dp through mdl-shadow--6dp '
                                                       'mdl-cell--9-col'})
    exercise_info = ''
    for label_p in information[0].contents[1].contents:
        if re.match('<p>(.*?)', str(label_p)) or re.match('<p><em>(.*?)', str(label_p)):
            if re.match('<strong>(.*?)', str(label_p.contents[0])):
                print("跳出寻找信息p标签循环")
                break
            else:
                if str(label_p.string) == 'None':
                    exercise_info = exercise_info + str(label_p)
                else:
                    exercise_info = exercise_info + str(label_p.string)
    exercise_info = exercise_info.replace('<p>', '\n').replace('</p>', '').replace('<em>', '').replace('<br/>', '\n').replace('</em>', '')

    param = {
        'page': url
    }
    # 难度
    try:
        d = requests.post(url_site, data=param, headers=header)
        difficulty = d.text.split('-')[1]
    except:
        difficulty = '未知'
    col.insert_one(
        {'id': i, 'exercise_title': title, 'exercise_info': exercise_info, 'JS_answer': code_js,
         'HTML_answer': code_html, 'difficulty': difficulty})
    print('page ' + str(i) + ' is done')
    i = i + 1
