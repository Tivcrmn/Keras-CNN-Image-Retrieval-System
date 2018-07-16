from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'_random', views.random_index)
]