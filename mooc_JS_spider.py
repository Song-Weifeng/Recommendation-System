import requests
import pandas as pd
import re
import time
import csv
from bs4 import BeautifulSoup

# url请求文件头
header = {
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
Cookie = {
    'Cookie': 'EDUWEBDEVICE=e88f62fb3eee4caeb4f2c8726bdb0823; __yadk_uid=0dV8q0AG1rqBtMLZFQLVGDSQT8vQ8VAu; '
              'WM_TID=0JAwbjdjKKZEVURFRUNtLNQq1vdfJfdc; MOOC_PRIVACY_INFO_APPROVED=true; hasVolume=true; '
              'videoVolume=0.8; videoRate=1; videoResolutionType=3; '
              '__guid=188523822.4165789100296653300.1618213146299.3677; NTESSTUDYSI=4b74675c2aa945389744f371a989f715; '
              'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1618213148,1618281808,1618366076; '
              'WM_NI=TY%2B8zUeyIoix8FalEm9Jzs%2B3WcyLoOVpg5L9s3N%2Fbi4vDwi1hnrXEND4JX3KBJJIw7Tvi'
              '%2B6YH76GofhJiIMWwp6Br2D5Ea4vplp2x6%2BHall3FXnXmYgh0sCRlq0q00YgQkw%3D; '
              'WM_NIKE'
              '=9ca17ae2e6ffcda170e2e6eea5e57298868287e95f89a88ab7c55e868e9baeae748d9cf7a5d539988697d4f32af0fea7c3b92a9887e5d9f95fa7a78790ec74fc9aaf8dc867fb96b694aa3995bdb7adee4596b0a9d6cf33b1ed82d0e163f8aa8c98ec3bacb2beb9c84688ec86b9b241829686aaf63d98aaa7ccb5538ce9faa8ee6eac96a7aad05db5b0faa3f13a88eb8b82b77eb4b4c0d3fb3ee998af8def398688a2b9f053a5b80094c25ab0af0092b33c9bb99f8cf637e2a3; monitor_count=24; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1618385317'}
url_comment = 'https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=4b74675c2aa945389744f371a989f715'
page = 1
data_pre1 = ['comment']
data_pre2 = pd.DataFrame(data_pre1)
data_pre2.to_csv('mooc_comment.csv', header=False, index=False, mode='a+')
while True:
    param = {
        'courseId': '1206706828',
        'pageIndex': page,
        'pageSize': '20',
        'orderBy': '3'
    }
    response = requests.post(url=url_comment, data=param, headers=header)
    if len(str(response.json()['result']['list'])) < 100:
        break
    j = 1
    for i in response.json()['result']['list']:
        print(i['content'])
        print('------------------------------------------------------------------')
        data1 = [(i['content'])]
        j = j + 1
        data2 = pd.DataFrame(data1)
        data2.to_csv('mooc_comment.csv', header=False, index=False, mode='a+')
    # if page == 19:
    #     break
    page = page + 1

