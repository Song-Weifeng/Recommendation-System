import heapq
import json
from flask import Flask, jsonify, make_response
from flask import request
import pymongo
import pandas as pd
import spacy

app = Flask(__name__)

nlp_zh = spacy.load("zh_core_web_md")
nlp_en = spacy.load('en_core_web_md')

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)

# 选择数据库
var_db = 'JS_exercise'
db = client[var_db]
# 切换库和集合
var_col = 'array'
col = client[var_db][var_col]


@app.route('/')
def hello_world():
    return 'Hello! World!'


@app.route('/start/Course', methods=["GET", "POST"])
def start_Course():
    """
    输入用户id
    冷启动的推荐课程，首先按照课程评分召回100个，然后根据用户标签排序
    :return:返回在全部题库中的最相似的n个课信息
        返回信息有：
            题目title，简介intro，链接url，封面链接face_url，评价得分score
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        search_Course_json = request.get_json()
        user_id = str(search_Course_json.get('user_id'))
        data = pd.read_csv('Course1.csv')
        data_list = data['video_title'].values.tolist()
        course_score = data['score'].values.tolist()
        course_id = data['id'].values.tolist()
        # print(course_score)
        max_score = heapq.nlargest(100, course_score)

        max_index_score = []
        max_index_100 = []
        max_title = []
        for item in max_score:
            index = course_score.index(item)
            max_index_100.append(index)
            max_title.append(data_list[index])
            max_index_score.append(course_id[index])
            course_score[index] = 0
        top_100_score = max_index_score
        # print('最大分数100堂课的索引是：')
        # print(max_index_100)
        # print('最大分数的100堂课的id是：')
        # print(top_100_score)
        # print('最大分数的100堂课的题目是：')
        # print(max_title)
        search_Course_similarity = []
        for item in max_title:
            doc1 = nlp_zh(client['User']['user_info'].find_one({"id": user_id})['tag'])
            doc2 = nlp_zh(item)
            search_Course_similarity.append(doc2.similarity(doc1))
        # print(heapq.nlargest(10, search_Course_similarity))
        max_number = heapq.nlargest(8, search_Course_similarity)
        max_index = []
        for item in max_number:
            index = search_Course_similarity.index(item)
            max_index.append(index)
            search_Course_similarity[index] = 0
        top_n = max_index
        # print(top_n)
        cols_list = client['Course'].list_collection_names()
        fe_title = []
        fe_info = []
        fe_url = []
        fe_score = []
        fe_face_url = []
        for index in top_n:
            for name in cols_list:
                if client['Course'][name].find_one({'id': top_100_score[index]}):
                    fe_title.append(client['Course'][name].find_one({'id': top_100_score[index]})['video_title'])
                    fe_info.append(client['Course'][name].find_one({'id': top_100_score[index]})['video_intro'])
                    fe_url.append(client['Course'][name].find_one({'id': top_100_score[index]})['video_url'])
                    fe_score.append(client['Course'][name].find_one({'id': top_100_score[index]})['score'])
                    fe_face_url.append(client['Course'][name].find_one({'id': top_100_score[index]})['video_face_url'])
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": [{'title': fe_title[0], 'info': fe_info[0], 'url': fe_url[0],
                      'score': fe_score[0], 'face_url': fe_face_url[0]},
                     {'title': fe_title[1], 'info': fe_info[1], 'url': fe_url[1],
                      'score': fe_score[1], 'face_url': fe_face_url[1]},
                     {'title': fe_title[2], 'info': fe_info[2], 'url': fe_url[2],
                      'score': fe_score[2], 'face_url': fe_face_url[2]},
                     {'title': fe_title[3], 'info': fe_info[3], 'url': fe_url[3],
                      'score': fe_score[3], 'face_url': fe_face_url[3]},
                     {'title': fe_title[4], 'info': fe_info[4], 'url': fe_url[4],
                      'score': fe_score[4], 'face_url': fe_face_url[4]},
                     {'title': fe_title[5], 'info': fe_info[5], 'url': fe_url[5],
                      'score': fe_score[5], 'face_url': fe_face_url[5]},
                     {'title': fe_title[6], 'info': fe_info[6], 'url': fe_url[6],
                      'score': fe_score[6], 'face_url': fe_face_url[6]},
                     {'title': fe_title[7], 'info': fe_info[7], 'url': fe_url[7],
                      'score': fe_score[7], 'face_url': fe_face_url[7]}]
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response



        # # top_n = list(map(search_Course_similarity.index, heapq.nlargest(10, search_Course_similarity)))  # 求最大的10个元素的索引
        #




#
# @app.route('/history_course', methods=['GET', 'POST'])
# def history_course():
#     '''
#     json参数：
#         'tag_course'课程类别
#         'id_course'课程id
#         'id_user'用户id
#     :return:
#     '''
#     if request.method == 'GET':
#         return '请使用POST请求'
#     else:
#         history_course_json = request.get_json()
#         history_course_col = client['User']['user_info']
#         tag_course = history_course_json.get('tag_course')
#         id_course = history_course_json.get('id_course')
#         id_user = history_course_json.get('id_user')
#         condition = {'id': id_user}
#         num = 0
#         try:
#             history_course_list = history_course_col.find_one(condition)['history_course']
#             print(history_course_list)
#             for item in history_course_list:
#                 if item.split('-')[0] == tag_course:
#                     new_item = item.split('-')[0] + '-' + item.split('-')[1] + '-' + str(int(item.split('-')[2]) + 1)
#                     index = history_course_list.index(item)
#                     history_course_list[index] = new_item
#                     history_course_col.update_one(condition, {'$set': {'history_course': history_course_list}})
#                     num += 1
#             if num == 0:
#                 history_course_list.append(tag_course + '-' + id_course + '-1')
#                 history_course_col.update_one(condition, {'$set': {'history_course': history_course_list}})
#             print(history_course_list)
#         except:
#             history_list = [tag_course + '-' + id_course + '-1']
#             history_course_col.update_one(condition, {'$set': {'history_course': history_list}})
#         return '1'
#
#
# @app.route('/tag_course', methods=['GET', 'POST'])
# def tag_course():
#     '''
#         传入参数json格式'tag_course'
#         :return: 所有该类别下的课程
#     '''
#     if request.method == 'GET':
#         return '请使用POST请求'
#     else:
#         tag_course_json = request.get_json()
#         col = client['Course'][tag_course_json.get('tag_course')]
#         item_list = []
#         for item in list(col.find()):
#             item_list.append(item)
#         print(item_list)
#         # 构建response对象
#         result = {
#             "stateCode": 200,
#             "message": "API调用成功",
#             "data": str(list(col.find()))
#         }
#         response = make_response(jsonify(result))
#         return response
#
# @app.route('/name', methods=['GET', 'POST'])
# def get_name():
#     item_list = []
#     for item in list(col.find()):
#         item_list.append(item)
#     print(item_list)
#     # 构建response对象
#     result = {
#         "stateCode": 200,
#         "message": "API调用成功",
#         "data": str(list(col.find()))
#     }
#     response = make_response(jsonify(result))
#     return response
#
#
# @app.route('/mypost', methods=["GET", "POST"])
# def get_gender():
#     if request.method == 'GET':
#         res = jsonify({'massage': [{'name': 'name1', 'words': 'words1'}, {'name': 'name2', 'words': 'words2'}]})
#         return res
#     else:
#         my_json = request.get_json()
#         print(my_json)
#         get_name = my_json.get("name")
#         get_age = my_json.get("age")
#         return jsonify(name=get_name, age=get_age)
#
#
# @app.route('/userProfile', methods=['GET', 'POST'])
# def get_profile():
#     if request.method == 'GET':
#         searchword = request.args.get('name', '')
#         print(searchword)
#         if searchword == '宋为峰':
#             return jsonify(user="宋为峰", pwd=999)
#         else:
#             return jsonify(user="宋", pwd=999)
#     elif request.method == 'POST':
#         print(request.form)
#         print(request.data)
#         print(request.json)
#         name = request.form.get('name')
#         if name == '宋为峰':
#             return jsonify(user='宋为峰', pwd=999)
#         else:
#             return jsonify(user='不是宋为峰', pwd=999)
#         # return '1'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
