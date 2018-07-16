
import numpy as np
import cv2
import os
from server import settings
from keras.models import model_from_json

def get_image_data(image_path):
    im = cv2.imread(os.path.join(settings.MEDIA_ROOT, image_path))
    im = cv2.resize(im, (224, 224)).astype(np.float32)
    im[:,:,0] -= 103.939
    im[:,:,1] -= 116.779
    im[:,:,2] -= 123.68
    return im

# 根据json文件和h5文件获得相应的模型
def load_model(model_name):
    # load json and create model
    json_file = open(os.path.join(settings.H5FILE_ROOT, model_name + '.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(os.path.join(settings.H5FILE_ROOT, model_name + '.h5'))
    print("Loaded model {0} from disk".format(model_name))
    return model

class VGGNet:
    def __init__(self):
        self.model_orig = load_model("model_pop4")
        self.model_bh = load_model("model_pop2")

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat(self, img_path):
        image_data = get_image_data(img_path)
        im = np.expand_dims(image_data, axis=0)
        pred = self.model_orig.predict(im)
        pred_bh = self.model_bh.predict(im)
        return (pred, pred_bh)


