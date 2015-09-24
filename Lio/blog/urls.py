from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^as/$', views.index, name='index'),
    url(r'^as/(\d{1,})/$', views.indexnum),
]
