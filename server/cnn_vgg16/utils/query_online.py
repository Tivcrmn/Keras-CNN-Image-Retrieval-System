# -*- coding: utf-8 -*-
from cnn_vgg16.utils.searcher import Searcher
import keras
import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from server import settings
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2'

DATABASE_PATH = os.path.join(settings.DATABASE_ROOT)

def get_image_path(path):
    images_path = [os.path.join(root, name)[58:]
                   for root, dirs, files in os.walk(path)
                   for name in files
                   if name.endswith((".jpg"))]
    return images_path

# 获取所有的图片的相对路径和101个标签
def get_image_labels(path, images_path):
    labels = []
    images_label = []
    for dirName, subdirList, fileList in os.walk(path):
        if dirName[-len('database'):]!="database" :
            newDir = dirName.split('/')[-1]
            labels.append(newDir)
    for img_path in images_path:
        img_dir = img_path.split('/')[-2]
        images_label.append(labels.index(img_dir))
    return labels, images_label

# 将所有图片的路径打乱并且返回同样顺序的标签
def randomize_data(images_label, images_path):
    #randomize order of data
    rnd_idx = range(len(images_label))
    rnd_idx = random.sample(rnd_idx, len(rnd_idx))

    images_label_t = [images_label[i] for i in rnd_idx]
    images_path_t = [images_path[i] for i in rnd_idx]
    return images_label_t, images_path_t

def query_online(isNew, name):
	images_path = get_image_path(DATABASE_PATH)
	labels, images_label = get_image_labels(DATABASE_PATH, images_path)
	images_label, images_path = randomize_data(images_label, images_path)
	# 将随机打乱的图片路径list和标签list组合成dict
	map_path_label = {}
	for image_path, image_label in zip(images_path, images_label):
	    map_path_label[image_path] = image_label
	searcher = Searcher(map_path_label=map_path_label, limit=100)
	print ("--------------------------------------------------")
	print ("               searching starts")
	print ("--------------------------------------------------")
	results = searcher.search(isNew, name, hamming_distance= 2)
	keras.backend.clear_session()
	return results