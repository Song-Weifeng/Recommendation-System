import requests
import pandas as pd
import time
import csv
from bs4 import BeautifulSoup
import re

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
url_1 = 'https://www.w3resource.com/python-exercises/python-basic-exercise-'
url_2 = '.php'
i = 1
while True:
    try:
        url = url_1 + str(i) + url_2
        page = requests.get(url, headers=header, cookies=Cookie)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find_all('h1', attrs={'class': 'heading'})
        answer = soup.find_all('code', attrs={'class': 'language-python'})
        information = soup.find_all('div', attrs={'class': 'mdl-cell mdl-card mdl-shadow--2dp through mdl-shadow--6dp '
                                                           'mdl-cell--9-col'})
        exercise_info = ''
        for label_p in information[0].contents[1].contents:
            if re.match('<p.*?>(.*?)</p>', str(label_p)):
                if str(label_p.string) == 'None':
                    # print(label_p)
                    exercise_info = exercise_info + str(label_p)
                else:
                    # print(label_p.string)
                    exercise_info = exercise_info + str(label_p.string)
        # print(title[0].string)
        # print(answer[0].string)
        if len(title[0].string) == 0:
            break
        data1 = [(i, title[0].string, exercise_info, answer[0].string)]
        data2 = pd.DataFrame(data1)
        data2.to_csv('python-basic-exercise.csv', header=False, index=False, mode='a+')
    except:
        print("Wrong!")
    print('page ' + str(i) + ' is done')
    i = i + 1
    time.sleep(2)

