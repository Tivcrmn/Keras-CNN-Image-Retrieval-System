from django.db import models

import mongoengine

class caltech101(mongoengine.Document):
    feature = mongoengine.BinaryField()
    hashcode = mongoengine.StringField()
    image_name = mongoengine.StringField()
    isInDatabase = mongoengine.BooleanField()
    intID = mongoengine.IntField()
