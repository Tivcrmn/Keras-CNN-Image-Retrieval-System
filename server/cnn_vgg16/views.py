import json
import os
import numpy as np
import base64
import random
from django.http import HttpResponse
from cnn_vgg16.utils.query_online import query_online
from server import settings
from cnn_vgg16.models import caltech101
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray)):
            return obj.tolist()
        elif isinstance(obj, bytes):  
            return str(obj, encoding='utf-8');  
        return json.JSONEncoder.default(self, obj)

def get_results(imgs):
    result = []
    for i, img in enumerate(imgs):
        if img[3]:
            path = settings.DATABASE_ROOT
        else:
            path = settings.MEDIA_ROOT
        f = open(os.path.join(path, img[2]),'rb')
        item = {"name": img[2], "base64": base64.b64encode(f.read()), "isInDatabase": img[3], "hashcode": img[1]}
        result.append(item)
        f.close()
    return result

def index(request):
    
    imgs = []
    if request.method == "POST":
        file_obj = request.FILES.get('file')
        f = open(os.path.join(settings.MEDIA_ROOT, file_obj.name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        imgs = query_online(True, file_obj.name)

    else:
        name = request.GET.get('name')
        imgs = query_online(False, name)
        
    result = get_results(imgs)
    return HttpResponse(json.dumps({"data": result}, cls=NumpyEncoder))

def random_index(request):
    imgs = []
    total = caltech101.objects.count()
    randomImg = caltech101.objects(intID=random.randint(1, total))
    imgs = query_online(False, randomImg[0]["image_name"])
    result = get_results(imgs)
    return HttpResponse(json.dumps({"data": result}, cls=NumpyEncoder))

