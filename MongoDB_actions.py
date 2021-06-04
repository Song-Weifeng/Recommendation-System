import pymongo  # 导入pymongo模块


# 第一种连接mongo数据库
# 第二种连接mongo数据库可以用url
def mongodb_init01():
    # 连接数据库
    mongo = pymongo.MongoClient(host='localhost', port=27017, tz_aware=True)

    # 选择数据库
    db = mongo.admin
    # 验证用户名
    db.authenticate("mongo", "swf5648413300")
    # 切换库
    db2 = mongo.testTT
    # collection = db2.user
    # collection.insert({"name": "张三"})
    # 删除库
    mongo.drop_database('testTT')
    # 获取数据库
    print(mongo.list_database_names())

    # # 选择集合
    # collection = db.users
    # # 插入数据
    # collection.insert({"name": "张三"})
    # print('1')


if __name__ == '__main__':
    mongodb_init01()
