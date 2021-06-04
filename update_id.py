import pymongo

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)

# # client['Course']['Python'].update_many({}, {'$inc': {"id": -1}})
# print(client['User']['user_info'].find_one({"id": '1'})['tag'])
fe = []
info = client['JS_exercise']['array'].find_one({'id': 1})
print(info)
fe.append(list(info))
print(fe[0]['id'])