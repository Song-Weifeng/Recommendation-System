import requests
import pandas as pd
from numpy import *
from snownlp import SnowNLP
import pymongo  # 导入pymongo模块

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
# 切换库
col = client.Course.Java
# 课程列表的请求文件头
header_list = {
    'authority': 'www.icourse163.org',
    'method': 'POST',
    'path': '/web/j/mocSearchBean.searchCourse.rpc?csrfKey=148b8f2c888f42ae956e6a99a9c5ed12',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '109',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'EDUWEBDEVICE=e88f62fb3eee4caeb4f2c8726bdb0823; WM_TID=0JAwbjdjKKZEVURFRUNtLNQq1vdfJfdc; MOOC_PRIVACY_INFO_APPROVED=true; hasVolume=true; videoVolume=0.8; videoRate=1; videoResolutionType=3; __guid=188523822.4165789100296653300.1618213146299.3677; NTESSTUDYSI=148b8f2c888f42ae956e6a99a9c5ed12; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1618213148,1618281808,1618366076,1618646627; WM_NI=KL6YdBtXV%2FTiYQU5eQVEN5RjHsyT0I%2FG5%2Fu82lOEjclR3bdoFYJvXZVM2wApSCIVaXeQwvkSbgQOa6eP35WYRKEY2FfjfrJSXVjLgfTuNyCiHbGzkeFMpb%2F1xKOovxX3a3A%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebaea7fb88d0084b76fb0968aa6c55f878f8bbbf474a3bffbdab879b3b48a91e52af0fea7c3b92a8994fabae74ab8889ad0d7639b8f9bd6e85b969b82d6d1628cadb7b5b343ed99fbd0f834f2b481a6e969b08efd83e76586878697db529693fe98c47c919d87b7e454a78fb997ea59a2b99fb0e43ea790fdd6d65392958bbab14ea6b6aa93c9599c8aa6ade66e98ab829ac2638cbe899bea6f8693c083ae3bbc958190f5749cedafd4c437e2a3; __yadk_uid=3X4KwjHGuqx1EWZHY0fElLgM291V7mOH; monitor_count=6; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1618648307',
    'edu-script-token': '148b8f2c888f42ae956e6a99a9c5ed12',
    'origin': 'https://www.icourse163.org',
    'referer': 'https://www.icourse163.org/search.htm?search=Java',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
url_course = 'https://www.icourse163.org/web/j/mocSearchBean.searchCourse.rpc?csrfKey=148b8f2c888f42ae956e6a99a9c5ed12'
param = {'mocCourseQueryVo': '{"keyword":"java","pageIndex":1,"highlight":true,"orderBy":0,"stats":30,"pageSize":20}'
         }
response_course = requests.post(url=url_course, data=param, headers=header_list)
list_num = 0
while True:
    if list_num == len(response_course.json()['result']['list']):
        print('跳出课程循环')
        break
    info = response_course.json()['result']['list'][list_num]
    shortName = info['mocCourseCard']['mocCourseCardDto']['schoolPanel']['shortName']
    course_id = info['mocCourseCard']['cid']
    course_info = info['mocCourseCard']['highlightContent']
    course_title = info['mocCourseCard']['mocCourseCardDto']['name']
    course_face = info['mocCourseCard']['mocCourseCardDto']['imgUrl']
    course_link = 'https://www.icourse163.org/course/' + \
                  str(shortName) + '-' + str(course_id) + '?from=searchPage'
    # 评论的请求文件头
    header_comment = {
        'authority': 'www.icourse163.org',
        'method': 'POST',
        'path': '/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=4b74675c2aa945389744f371a989f715',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '53',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'EDUWEBDEVICE=e88f62fb3eee4caeb4f2c8726bdb0823; __yadk_uid=0dV8q0AG1rqBtMLZFQLVGDSQT8vQ8VAu; WM_TID=0JAwbjdjKKZEVURFRUNtLNQq1vdfJfdc; MOOC_PRIVACY_INFO_APPROVED=true; hasVolume=true; videoVolume=0.8; videoRate=1; videoResolutionType=3; __guid=188523822.4165789100296653300.1618213146299.3677; NTESSTUDYSI=4b74675c2aa945389744f371a989f715; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1618213148,1618281808,1618366076; WM_NI=TY%2B8zUeyIoix8FalEm9Jzs%2B3WcyLoOVpg5L9s3N%2Fbi4vDwi1hnrXEND4JX3KBJJIw7Tvi%2B6YH76GofhJiIMWwp6Br2D5Ea4vplp2x6%2BHall3FXnXmYgh0sCRlq0q00YgQkw%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea5e57298868287e95f89a88ab7c55e868e9baeae748d9cf7a5d539988697d4f32af0fea7c3b92a9887e5d9f95fa7a78790ec74fc9aaf8dc867fb96b694aa3995bdb7adee4596b0a9d6cf33b1ed82d0e163f8aa8c98ec3bacb2beb9c84688ec86b9b241829686aaf63d98aaa7ccb5538ce9faa8ee6eac96a7aad05db5b0faa3f13a88eb8b82b77eb4b4c0d3fb3ee998af8def398688a2b9f053a5b80094c25ab0af0092b33c9bb99f8cf637e2a3; monitor_count=26; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1618385700',
        'origin': 'https://www.icourse163.org',
        'referer': 'https://www.icourse163.org/course/HCIT-1206706828?from=searchPage',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    url_comment = 'https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=4b74675c2aa945389744f371a989f715'
    page = 1
    data_pre1 = ['comment']
    data_pre2 = pd.DataFrame(data_pre1)
    data_pre2.to_csv('mooc_comment.csv', header=False, index=False, mode='a+')

    while True:
        print('评论循环第'+str(page)+'页')
        param = {
            'courseId': course_id,
            'pageIndex': page,
            'pageSize': '20',
            'orderBy': '3'
        }
        response_comment = requests.post(url=url_comment, data=param, headers=header_comment)

        if len(str(response_comment.json()['result']['list'])) < 100:
            print('跳出评论循环')
            break
        j = 1
        for i in response_comment.json()['result']['list']:
            data1 = [(i['content'])]
            j = j + 1
            data2 = pd.DataFrame(data1)
            data2.to_csv('mooc_comment.csv', header=False, index=False, mode='a+')
        page = page + 1

    df = pd.read_csv('mooc_comment.csv', header=None, usecols=[0])
    contents = df.values.tolist()
    score = []
    for content in contents:
        try:
            s = SnowNLP(content[0])
            score.append(s.sentiments)
        except:
            print('Wrong!')
            score.append(0.5)
    average = mean(score)
    print(average)
    col.insert_one(
        {'id': list_num + 1, 'video_url': course_link, 'video_face_url': course_face, 'video_title': course_title,
         'video_intro': course_info, 'score': average})
    list_num = list_num + 1
    os.remove('mooc_comment.csv')
