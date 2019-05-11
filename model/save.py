# -*- coding: UTF-8 -*-
from bson.binary import Binary  
import pymongo
import pickle

with open("index.pickle-vgg19-1_fast", "rb") as f:
    index_fast = pickle.load(f, encoding='latin1')
# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient("mongodb://user:123456@ds217360.mlab.com:17360/capstone")

#连接到数据库myDatabase
DATABASE = "capstone"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "caltech101"
db_coll = db[COLLECTION]
index = 1
for key in index_fast.keys():
    images = index_fast[key]
    print("begin save key", key)
    for image_path, feature in images:
        db_coll.insert_one({"feature": Binary(pickle.dumps(feature, protocol=-1), subtype=128), "hashcode": key, "image_path": "http://p8earzm4w.bkt.clouddn.com/" + image_path[21:], "image_name": image_path[21:], "isInDatabase": True, "intID": index})
        index += 1;
print("all key have saved")

# data = db_coll.find_one({"image_path": "101_ObjectCategories/grand_piano/image_0095.jpg"})

# my_db_nparray = pickle.loads(data['feature'])
# print(my_db_nparray.shape)
