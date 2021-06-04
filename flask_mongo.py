from flask import Flask, jsonify, make_response
from flask import request
import pymongo
import pandas as pd
# import findspark
# from pyspark.sql import functions as F
# from pyspark.sql import types as T
# from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from scipy.spatial import distance
import spacy
import heapq
import os

nlp_zh = spacy.load("zh_core_web_md")
nlp_en = spacy.load('en_core_web_md')

# findspark.init()
# from pyspark.sql import SparkSession

app = Flask(__name__)
# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
# spark = SparkSession \
#     .builder \
#     .appName("PySpark flask") \
#     .getOrCreate()
# sc = spark.sparkContext


@app.route('/')
def hello_world():
    return jsonify(title='hello world')


@app.route('/history_course', methods=['GET', 'POST'])
def history_course():
    """
    json参数：
        'tag_course'课程类别
        'id_course'课程id
        'id_user'用户id
    :return:
        数据库格式：课程类别 - 课程id - 该用户浏览次数 eg.C-2-1为给用户浏览了C语言类别的id为2的题1次
        使用方法：每点击一次某课程链接就post给这个网址以上规定json参数，实现更改数据库内容
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        history_course_json = request.get_json()
        history_course_col = client['User']['user_info']
        tag_course = history_course_json.get('tag_course')
        id_course = history_course_json.get('id_course')
        id_user = history_course_json.get('id_user')
        condition = {'id': id_user}
        num = 0
        try:
            history_course_list = history_course_col.find_one(condition)['history_course']
            print(history_course_list)
            for item in history_course_list:
                if item.split('-')[0] == tag_course:
                    new_item = item.split('-')[0] + '-' + item.split('-')[1] + '-' + str(int(item.split('-')[2]) + 1)
                    index = history_course_list.index(item)
                    history_course_list[index] = new_item
                    history_course_col.update_one(condition, {'$set': {'history_course': history_course_list}})
                    num += 1
            if num == 0:
                history_course_list.append(tag_course + '-' + id_course + '-1')
                history_course_col.update_one(condition, {'$set': {'history_course': history_course_list}})
        except:
            history_list = [tag_course + '-' + id_course + '-1']
            history_course_col.update_one(condition, {'$set': {'history_course': history_list}})
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功"
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return '1'


@app.route('/tag/exercise', methods=['GET', 'POST'])
def tag_exercise():
    """
    传入参数json格式’tag_exercise‘
    :return: 所有该类别下的题目
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        tag_exercise_json = request.get_json()
        col = client['JS_exercise'][tag_exercise_json.get('tag_exercise')]
        item_list = []
        x = list(col.find())
        for item in x:
            item_list.append(item)
        print(item_list)
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": str(x)
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response


@app.route('/tag/course', methods=['GET', 'POST'])
def tag_course():
    """
        传入参数json格式'tag_course'
        :return: 所有该类别下的课程
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        tag_course_json = request.get_json()
        col = client['Course'][tag_course_json.get('tag_course')]
        item_list = []
        x = list(col.find())
        for item in x:
            item_list.append(item)
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": str(x)
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response


@app.route('/search/JS_exercise', methods=["GET", "POST"])
def search_JS_exercise():
    """
    输入一个js编程中的英文字符串search_exercise ，根据spacy英文模型的相似度计算相似度
    :return: 返回三个与输入相似度最大的题目用于前端重新读取数据库显示在页面上
        返回信息有：题目title，简介intro，html答案HTML_answer,js答案js_answer，级别level，难度difficulty，类别label
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        search_JS_exercise_json = request.get_json()
        var_db = 'JS_exercise'
        data = pd.read_csv('JS_exercise.csv')
        data_list = data['exercise_title'].values.tolist()
        data_id = data['id'].values.tolist()
        cols_list = client[var_db].list_collection_names()
        # print(cols_list)
        search_exercise = search_JS_exercise_json.get("search_exercise")
        similarity = []
        doc2 = nlp_en(search_exercise)
        for item in data_list:
            doc1 = nlp_en(item)
            similarity.append(doc1.similarity(doc2))
        # print(similarity)
        max_number = heapq.nlargest(3, similarity)
        max_index = []
        for item in max_number:
            index = similarity.index(item)
            max_index.append(index)
            similarity[index] = 0
        top_n = max_index
        fe = []
        for index in top_n:
            for name in cols_list:
                info = client['JS_exercise'][name].find_one({'id': data_id[index]})
                if info:
                    fe.append(info)
                    break

        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": [{'title': fe[0]['exercise_title'], 'info': fe[0]['exercise_info'], 'JS_answer': fe[0]['JS_answer'],
                      'HTML_answer': fe[0]['HTML_answer'], 'difficulty': fe[0]['difficulty'], 'level': fe[0]['level'],
                      'label': fe[0]['label']},
                     {'title': fe[1]['exercise_title'], 'info': fe[1]['exercise_info'], 'JS_answer': fe[1]['JS_answer'],
                      'HTML_answer': fe[1]['HTML_answer'], 'difficulty': fe[1]['difficulty'], 'level': fe[1]['level'],
                      'label': fe[1]['label']},
                     {'title': fe[2]['exercise_title'], 'info': fe[2]['exercise_info'], 'JS_answer': fe[2]['JS_answer'],
                      'HTML_answer': fe[2]['HTML_answer'], 'difficulty': fe[2]['difficulty'], 'level': fe[2]['level'],
                      'label': fe[2]['label']}]
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response


@app.route('/search/Course', methods=["GET", "POST"])
def search_Course():
    """
    传入搜索框内容参数search_Course
    :return:返回在全部课程中的最相似的3个课信息
        返回信息有：
            题目title，简介intro，链接url，封面链接face_url，评价得分score
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        search_Course_json = request.get_json()
        search_Course = search_Course_json.get('search_Course')
        data = pd.read_csv('Course1.csv')
        data_list = data['video_title'].values.tolist()
        data_id = data['id'].values.tolist()
        search_Course_similarity = []
        for item in data_list:
            doc1 = nlp_zh(search_Course)
            doc2 = nlp_zh(item)
            search_Course_similarity.append(doc2.similarity(doc1))
        print(heapq.nlargest(10, search_Course_similarity))
        max_number = heapq.nlargest(3, search_Course_similarity)
        max_index = []
        for item in max_number:
            index = search_Course_similarity.index(item)
            print(data_list[index])
            max_index.append(index)
            search_Course_similarity[index] = 0
        top_n = max_index
        print(top_n)
        cols_list = client['Course'].list_collection_names()
        fe = []
        for index in top_n:
            for name in cols_list:
                info = client['Course'][name].find_one({'id': data_id[index]})
                if info:
                    fe.append(info)
                    break
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": [{'title': fe[0]['video_title'], 'info': fe[0]['video_intro'], 'url': fe[0]['video_url'],
                      'score': fe[0]['score'], 'face_url': fe[0]['video_face_url']},
                     {'title': fe[1]['video_title'], 'info': fe[1]['video_intro'], 'url': fe[1]['video_url'],
                      'score': fe[1]['score'], 'face_url': fe[1]['video_face_url']},
                     {'title': fe[2]['video_title'], 'info': fe[2]['video_intro'], 'url': fe[2]['video_url'],
                      'score': fe[2]['score'], 'face_url': fe[2]['video_face_url']}]
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response


@app.route('/word2vec', methods=["GET", "POST"])
def word2vec():
    """
        输入一个js题目的id,返回根据word2vec算出的它的相似的题的id
        :return:
    """
    if request.method == 'GET':
        return '请使用POST请求'
    else:
        # spark = SparkSession \
        #     .builder \
        #     .appName("PySpark flask") \
        #     .getOrCreate()
        # sc = spark.sparkContext
        df = pd.read_csv("JS_exercise_embedding.csv")
        df["word2vec"] = df["word2vec"].map(lambda x: np.array(json.loads(x)))
        # print(df.head(20))
        word2vec_json = request.get_json()
        title_id = int(word2vec_json.get('title_id'))
        # title_id = 1
        item_embedding = df.loc[df["id"] == title_id, "word2vec"].iloc[0]
        # df["sim_value"] = df["word2vec"].map(lambda x: 1 - distance.cosine(item_embedding, x))
        df["sim_value"] = df["word2vec"].map(lambda x: np.corrcoef(np.vstack([item_embedding, x]))[0][1])
        recommend = df.sort_values(by="sim_value", ascending=False).head(10)
        # print(df.sort_values(by="sim_value", ascending=False))
        cols_list = client['JS_exercise'].list_collection_names()
        fe = []
        # fe_title = []
        # fe_info = []
        # fe_js_answer = []
        # fe_HTML_answer = []
        # fe_difficulty = []
        # fe_level = []
        # fe_label = []
        print(list(recommend['id']))
        for index in list(recommend['id']):
            # print('开始搜新的一个')
            # print(index)
            for name in cols_list:
                # print('新的一个集合')
                # print(name)
                info = client['JS_exercise'][name].find_one({'id': index})
                if info is not None:
                    # print('搜到了')
                    # print(name)
                    # print(index)
                    # fe_title.append(info['exercise_title'])
                    # fe_info.append(info['exercise_info'])
                    # fe_js_answer.append(info['JS_answer'])
                    # fe_HTML_answer.append(info['HTML_answer'])
                    # fe_difficulty.append(info['difficulty'])
                    # fe_level.append(info['level'])
                    # fe_label.append(info['label'])
                    fe.append(info)
                    break
        print(fe)
        # 构建response对象
        result_word2vec = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": [{'title': fe[1]['exercise_title'], 'info': fe[1]['exercise_info'], 'JS_answer': fe[1]['JS_answer'],
                      'HTML_answer': fe[1]['HTML_answer'], 'difficulty': fe[1]['difficulty'], 'level': fe[1]['level'],
                      'label': fe[1]['label']},
                     {'title': fe[2]['exercise_title'], 'info': fe[2]['exercise_info'], 'JS_answer': fe[2]['JS_answer'],
                      'HTML_answer': fe[2]['HTML_answer'], 'difficulty': fe[2]['difficulty'], 'level': fe[2]['level'],
                      'label': fe[2]['label']},
                     {'title': fe[3]['exercise_title'], 'info': fe[3]['exercise_info'], 'JS_answer': fe[3]['JS_answer'],
                      'HTML_answer': fe[3]['HTML_answer'], 'difficulty': fe[3]['difficulty'], 'level': fe[3]['level'],
                      'label': fe[3]['label']}]
        }
        response = make_response(jsonify(result_word2vec))
        # print(response)
        # print('最后一步')
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response


@app.route('/start/Course', methods=["GET", "POST"])
def start_Course():
    """
    输入用户id
    冷启动的推荐课程，首先按照课程评分召回100个，然后根据用户标签排序
    :return:返回在全部题库中的最相似的8个课信息
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
        x = client['User']['user_info'].find_one({"id": user_id})
        print(x['tag'])
        for item in max_title:
            doc1 = nlp_zh(x['tag'])
            doc2 = nlp_zh(item)
            search_Course_similarity.append(doc2.similarity(doc1))
        max_number = heapq.nlargest(8, search_Course_similarity)
        max_index = []
        print(search_Course_similarity)
        test1 = search_Course_similarity.copy()
        for item in max_number:
            index = search_Course_similarity.index(item)
            max_index.append(index)
            search_Course_similarity[index] = 0
        top_n = max_index
        print(max_index)

        cols_list = client['Course'].list_collection_names()
        fe = []
        for index in top_n:
            for name in cols_list:
                info = client['Course'][name].find_one({'id': top_100_score[index]})
                if info:
                    fe.append(info)
                    break
        # 构建response对象
        result = {
            "stateCode": 200,
            "message": "API调用成功",
            "data": [{'title': fe[0]['video_title'], 'info': fe[0]['video_intro'], 'url': fe[0]['video_url'],
                      'score': fe[0]['score'], 'face_url': fe[0]['video_face_url']},
                     {'title': fe[1]['video_title'], 'info': fe[1]['video_intro'], 'url': fe[1]['video_url'],
                      'score': fe[1]['score'], 'face_url': fe[1]['video_face_url']},
                     {'title': fe[2]['video_title'], 'info': fe[2]['video_intro'], 'url': fe[2]['video_url'],
                      'score': fe[2]['score'], 'face_url': fe[2]['video_face_url']},
                     {'title': fe[3]['video_title'], 'info': fe[3]['video_intro'], 'url': fe[3]['video_url'],
                      'score': fe[3]['score'], 'face_url': fe[3]['video_face_url']},
                     {'title': fe[4]['video_title'], 'info': fe[4]['video_intro'], 'url': fe[4]['video_url'],
                      'score': fe[4]['score'], 'face_url': fe[4]['video_face_url']},
                     {'title': fe[5]['video_title'], 'info': fe[5]['video_intro'], 'url': fe[5]['video_url'],
                      'score': fe[5]['score'], 'face_url': fe[5]['video_face_url']},
                     {'title': fe[6]['video_title'], 'info': fe[6]['video_intro'], 'url': fe[6]['video_url'],
                      'score': fe[6]['score'], 'face_url': fe[6]['video_face_url']},
                     {'title': fe[7]['video_title'], 'info': fe[7]['video_intro'], 'url': fe[7]['video_url'],
                      'score': fe[7]['score'], 'face_url': fe[7]['video_face_url']}]
        }
        response = make_response(jsonify(result))
        # 设置响应请求头
        response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
        response.headers["Access-Control-Allow-Methods"] = 'POST, GET'  # 允许的请求方法
        response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

        return response

        # # top_n = list(map(search_Course_similarity.index, heapq.nlargest(10, search_Course_similarity)))  # 求最大的10个元素的索引
        #


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
