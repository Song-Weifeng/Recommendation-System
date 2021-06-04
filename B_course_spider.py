import requests
import time
from bs4 import BeautifulSoup
import re
import pymongo
import pandas as pd

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
# 切换库
col = client.Course.JavaScript

# 文件请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
                  'Safari/537.36'}
Cookie = {
    'Cookie': "_uuid=33F0119A-6E16-E299-258C-7C881BEE969994823infoc; "
              "buvid3=EC9D89B1-6E13-4519-8C6C-1AE65E549C6F155841infoc; sid=d5vt0eby; LIVE_BUVID=AUTO8615877207428382; "
              "rpdid=|(~uuJkYk|u0J'ul)~~k|~mk; blackside_state=1; CURRENT_FNVAL=80; DedeUserID=46547619; "
              "DedeUserID__ckMd5=b40a2ece881a2445; SESSDATA=3f03ae98%2C1618826387%2C1784f*a1; "
              "bili_jct=d89ea97667c3fd4ef0d3402af9136604; buivd_fp=EC9D89B1-6E13-4519-8C6C-1AE65E549C6F155841infoc; "
              "buvid_fp_plain=EC9D89B1-6E13-4519-8C6C-1AE65E549C6F155841infoc; "
              "__guid=88747417.2457128004095905300.1614061629475.0554; "
              "buvid_fp=EC9D89B1-6E13-4519-8C6C-1AE65E549C6F155841infoc; CURRENT_QUALITY=80; "
              "fingerprint3=da4a2b92b7172d8e9000322de840daac; fingerprint=e75683c366a2ead6456e80522a77275e; "
              "fingerprint_s=9407a994e9af8800b8751ccd37ed4bfe; bp_video_offset_46547619=512344969417874864; "
              "bp_t_offset_46547619=512344969417874864; bsource=search_360; finger=158939783; arrange=matrix; PVID=1; "
              "monitor_count=5 "}
# 课程内部url
course_url = 'https://www.bilibili.com/video/'
# 请求视频封面的网站
site_face = "https://api.bilibili.com/x/web-interface/view?bvid="
j = 1
while True:
    if j == 3:
        break
    try:
        # 课程视频列表的url
        url_0 = 'https://search.bilibili.com/all?keyword=JavaScript&from_source=nav_search_new&page='
        url = url_0 + str(j)
        print('page ' + str(j) + ' 开始：')
        j = j + 1
        # 主界面
        page = requests.get(url, headers=header, cookies=Cookie)
        # BeautifulSoup解析网址 视频列表页面
        soup = BeautifulSoup(page.content, 'html.parser')
        i = 0
        while True:
            if i == 20:
                break
            # 视频网址
            video_url = soup.find_all('a', attrs={'class': 'title'})[i].get('href')
            video_url = 'http:' + video_url
            # 浏览量
            video_watch_num = soup.find_all('span', attrs={'class': 'so-icon watch-num'})[i].contents[1]
            video_watch_num = str(video_watch_num).split('\n')[1].split(' ')[8]
            # bv号
            bv_id = re.split('[/?]', video_url)[4]
            # 视频封面url
            video_face_url = requests.get(site_face + str(bv_id), headers=header, cookies=Cookie).json()['data']['pic']
            # 视频名称
            video_title = soup.find_all('a', attrs={'class': 'title'})[i].get('title')
            # 视频内部界面
            page_inter = requests.get(course_url + str(bv_id), headers=header, cookies=Cookie)
            # BeautifulSoup解析网址 视频内部页面
            soup_inter = BeautifulSoup(page_inter.content, 'html.parser')
            # 视频简介
            video_intro_pre = soup_inter.find_all('div', attrs={'class': 'info open'})[0].contents
            video_intro = ''
            for string in video_intro_pre:
                video_intro = video_intro + str(string)
            # print(video_url)  # 视频网址
            # print(video_face_url)  # 视频封面图片地址
            # print(video_title)  # 视频名称
            # print(video_intro)  # 视频简介
            # print(video_watch_num)  # 视频浏览量
            col.insert_one(
                {'id': (j - 1)*10 + i + 1, 'video_url': video_url, 'video_face_url': video_face_url, 'video_title': video_title,
                 'video_intro': video_intro, 'video_watch_num': video_watch_num})
            i = i + 1
            print(' item ' + str(i) + ' is done')
    except:
        print("Wrong!")
