from django.conf.urls import url
from django.conf.urls import include, url
#from allauth.account import views as allauthviews
from . import views
import os
#from allauth.socialaccount.views import SignupView

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'csr-request/', views.csrrequest, name='csrrequest'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^upload-certificate/', views.list, name='list'),
    url(r'^profile1/', views.profile1, name='profile1'),
    url(r'^profile2/', views.profile2, name='profile2'),
    url(r'^prodinstances/', views.prodinstances, name='prodinstances'),
]
