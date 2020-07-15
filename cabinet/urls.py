from django.urls import path
from . import views
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^$', views.send, name='invoice'),
    url(r'^invoice/$', views.send, name='invoice'),
    url(r'^createuser/$', views.createuser, name='createuser'),
    #url(r'^filter/$', views.FilterListView.as_view(), name='filter'),
    #url(r'^filter/$', views.filter, name='filter'),
    url(r'^send/$', views.send, name='send'),
    url(r'^register/$', views.register, name='register')
]

