import requests
import json

url_site = 'https://www.w3resource.com/assets/level_display.php'
url_1 = 'https://www.w3resource.com/javascript-exercises/javascript-basic-exercise-'

url_2 = '.php'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
i = 1
while i < 50:
    url_d = url_1 + str(i) + url_2

    param = {
        'page': url_d
    }
    response = requests.post(url=url_site, data=param, headers=headers)

    difficulty = response.text
    print('题目'+str(i)+'难度为： ' + difficulty)
    i = i + 1
