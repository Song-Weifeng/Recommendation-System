# encoding=gbk

import requests
import pandas as pd
import re
import time
import csv
from bs4 import BeautifulSoup
import os
from urllib import request

# url�����ļ�ͷ
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
# �Ѷ�
url_site = 'https://www.w3resource.com/assets/level_display.php'
# url_D1 = 'https://www.w3resource.com/javascript-exercises/javascript-basic-exercise-'
# url_D2 = '.php'
# # ͼƬ����
# url_P1 = 'https://www.w3resource.com/w3r_images/javascript-string-image-exercise-'
# url_P2 = '.png'
# ����ͼ
# url_F1 = 'https://www.w3resource.com/w3r_images/javascript-string-exercise-'
# url_F2 = '.png'
i = 1
while True:
    # ƴ��url
    # ������
    url = url_1 + str(i) + url_2
    # �Ѷ�
    url_D = url
    param = {
        'page': url_D
    }
    # # ͼ�α�ʾ
    # url_P = url_P1 + str(i) + url_P2
    # # ����ͼ
    # url_F = url_F1 + str(i) + url_F2
    try:
        # request����
        # ������
        html_solution = requests.get(url, headers=header, cookies=Cookie)
        # �Ѷ�
        Get_difficulty = requests.post(url_site, data=param, headers=header)
        # ͼ�α�ʾ
        # html_P = requests.get(url_P, headers=header, cookies=Cookie)
        # BeautifulSoup������ַ
        soup = BeautifulSoup(html_solution.content, 'html.parser')
        # soup_P = BeautifulSoup(html_P.content, 'html.parser')
        # ��Ŀ
        title = soup.find_all('h1', attrs={'class': 'heading'})
        print(title[0].string)
        # �Ѷ�
        difficulty = Get_difficulty.text
        dd = difficulty.split('-')
        print(dd[1])
        # html����
        code_html = soup.find_all('code', attrs={'class': 'language-html'})
        # js����
        code_js = soup.find_all('code', attrs={'class': 'language-js'})
        # # ͼ�α�ʾ
        # p = requests.get(url_P)
        # with open('E:/Reactѧϰ/cn42/61-Guided-Practice/src/picture/js/Pictorial Presentation/' + 'js-' + str(i) + '.png', 'wb') as file:
        #     file.write(p.content)
        # p = requests.get(url_F)
        # with open('E:/Reactѧϰ/cn42/61-Guided-Practice/src/picture/js/Flowchart/' + 'js-' + str(i) + '.png', 'wb') as file:
        #     file.write(p.content)
        # ����ѭ����ֹ����
        if len(title) == 0:
            break
        for jj in range(len(title)):
            data1 = [(i, title[jj].string, code_html[jj].string, code_js[jj].string, dd[1])]
            data2 = pd.DataFrame(data1)
            data2.to_csv('E:/Reactѧϰ/cn42/61-Guided-Practice/src/ml-latest-small/JavaScript_Basic.csv', header=False, index=False, mode='a+')
    except:
        print("Wrong!")
    print('page ' + str(i) + ' is done')
    i = i + 1
    time.sleep(2)
