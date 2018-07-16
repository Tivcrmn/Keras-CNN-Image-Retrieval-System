import numpy
import time
from sklearn.preprocessing import normalize
import cv2
import os
import numpy as np
from server import settings
from bson.binary import Binary  
from cnn_vgg16.models import caltech101
from cnn_vgg16.utils.VGG19 import VGGNet
import pickle

class Searcher:
    def __init__(self, map_path_label, limit=10):
        # store our index path
        self.limit = limit
        self.map_path_label = map_path_label
        self.hash_str = lambda x: '1' if x==1 else '0'
        
    def chi2_distance(self, histA, histB, eps = 1e-10):
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])
        return d
    
    def hamming_distance(self, a, b):
        cnt=0
        for i ,j in zip(a, b):
            if i!=j:
                cnt+=1
        return cnt

    def search(self, isNew, image_path, hamming_distance = 1):
        results = self.search_with_hash(isNew, image_path, hamming_distance)
        return results
    
    def search_with_hash(self, isNew, image_path, hamming_distance):
        
        results = {}
        hashList = caltech101.objects.distinct('hashcode')
        if isNew:
            model = VGGNet()
            (queryFeatures, pred_bh) = model.extract_feat(image_path)
            queryHash = normalize(pred_bh)
            queryHash[queryHash>=0.5]=1
            queryHash[queryHash<0.5]=0
            queryHash = ''.join([self.hash_str(i) for i in queryHash[0]])
        else:
            query = caltech101.objects(image_name=image_path)
            queryFeatures = pickle.loads(query[0]['feature'])
            queryHash = query[0]['hashcode']
                

        for key in hashList:
            if self.hamming_distance(queryHash, key) <= hamming_distance:
                images_path = caltech101.objects(hashcode=key)
                for image in images_path:
                    d = self.chi2_distance(pickle.loads(image['feature']), queryFeatures)
                    results[image['image_name']] = (key, d, image['isInDatabase'])

        results = sorted([(v[1], v[0], k, v[2]) for (k,v) in results.items()])
        results = results[:self.limit]
        return results
