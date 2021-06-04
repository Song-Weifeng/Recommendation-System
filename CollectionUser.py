# encoding=gbk

import requests
import pandas as pd
import re
import time
import csv
from bs4 import BeautifulSoup
import os
from urllib import request

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
url_1 = 'https://www.w3resource.com/javascript-exercises/javascript-basic-exercise-'
url_2 = '.php'
# 难度
url_site = 'https://www.w3resource.com/assets/level_display.php'
# url_D1 = 'https://www.w3resource.com/javascript-exercises/javascript-basic-exercise-'
# url_D2 = '.php'
# # 图片描述
# url_P1 = 'https://www.w3resource.com/w3r_images/javascript-string-image-exercise-'
# url_P2 = '.png'
# 流程图
# url_F1 = 'https://www.w3resource.com/w3r_images/javascript-string-exercise-'
# url_F2 = '.png'
i = 1
while True:
    # 拼接url
    # 主界面
    url = url_1 + str(i) + url_2
    # 难度
    url_D = url
    param = {
        'page': url_D
    }
    # # 图形表示
    # url_P = url_P1 + str(i) + url_P2
    # # 流程图
    # url_F = url_F1 + str(i) + url_F2
    try:
        # request请求
        # 主界面
        html_solution = requests.get(url, headers=header, cookies=Cookie)
        # 难度
        Get_difficulty = requests.post(url_site, data=param, headers=header)
        # 图形表示
        # html_P = requests.get(url_P, headers=header, cookies=Cookie)
        # BeautifulSoup解析网址
        soup = BeautifulSoup(html_solution.content, 'html.parser')
        # soup_P = BeautifulSoup(html_P.content, 'html.parser')
        # 题目
        title = soup.find_all('h1', attrs={'class': 'heading'})
        print(title[0].string)
        # 难度
        difficulty = Get_difficulty.text
        dd = difficulty.split('-')
        print(dd[1])
        # html代码
        code_html = soup.find_all('code', attrs={'class': 'language-html'})
        # js代码
        code_js = soup.find_all('code', attrs={'class': 'language-js'})
        # # 图形表示
        # p = requests.get(url_P)
        # with open('E:/React学习/cn42/61-Guided-Practice/src/picture/js/Pictorial Presentation/' + 'js-' + str(i) + '.png', 'wb') as file:
        #     file.write(p.content)
        # p = requests.get(url_F)
        # with open('E:/React学习/cn42/61-Guided-Practice/src/picture/js/Flowchart/' + 'js-' + str(i) + '.png', 'wb') as file:
        #     file.write(p.content)
        # 设置循环终止变量
        if len(title) == 0:
            break
        for jj in range(len(title)):
            data1 = [(i, title[jj].string, code_html[jj].string, code_js[jj].string, dd[1])]
            data2 = pd.DataFrame(data1)
            data2.to_csv('E:/React学习/cn42/61-Guided-Practice/src/ml-latest-small/JavaScript_Basic.csv', header=False, index=False, mode='a+')
    except:
        print("Wrong!")
    print('page ' + str(i) + ' is done')
    i = i + 1
    time.sleep(2)
