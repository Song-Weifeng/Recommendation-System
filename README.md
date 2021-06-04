# Recommendation-System
本科毕设-基于用户兴趣和行为的智能选课和练习系统
# 基于用户兴趣与行为的智能选课和练习系统

## 开发环境

Python3.8、MongoDB数据库

## 数据信息

### 数据库：

课程、题目、用户三个数据库

课程来自于中国大学MOOC网站、题目来自于www.w3resource.com

详细信息论文里有写

注意：因为数据库被黑，只有每条数据中需要计算的部分留了下来形成文件，因此需要重新运行爬虫文件去获取

### 代码运行前提前准备的csv文件：

收集课程评论的文件sentiment.csv

提前训练好的词向量文件JS_exercise_embedding.csv

课程id与名称的两列文件Course1.csv

## 文件描述（所用代码文件夹）

### ml-lastest-small

该文件夹是一个开源的用户与电影数据集，在做实验的过程中往里面添加了题库的数据以及各种数据之间的组合文件

其中的readme文件是原数据集的描述文件

### picture

该文件中是爬虫获取的题目的流程图以及题目示意图

### tool_flask

该文件中是本项目中的flask框架部分

flask_mongo是核心代码，JianDanHouDuan是尝试各种功能所用的实验文件

### tool_mongo

该文件中是本项目中MongoDB的操作文件

包括将数据库中的文件转换为本地csv文件以及数据库的各种操作等

tool_spider

该文件中是本项目中用到的爬虫工具的文件从名字上基本可以看出每个文件是做什么的

以finnal开头的两个文件是最终文件。但使用时仍需要实时更改一些参数

推荐观看B站up【龙王山小青椒】的教学视频，内包括该项目中用到的情感分析实例

https://www.bilibili.com/video/BV18C4y1H7mr

### tool_word2vec

该文件中是本项目中用到的训练word2vec模型的文件以及一些绘制推荐系统性能指标的文件

推荐观看B站up【蚂蚁学Python】

了解推荐系统基础知识https://www.bilibili.com/video/BV1Dz411B7wd

word2vec模型https://www.bilibili.com/video/BV1th411Z7eG

关于推荐系统性能指标可以在图书馆看《深度学习与推荐系统》或者上网查找

### Sentiment_analysis.py

该文件是对课程的评论进行情感分析



