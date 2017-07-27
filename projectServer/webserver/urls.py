
from django.conf.urls import url
from django.contrib import admin
from myApp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index.html',views.index),
    url(r'^register',views.register),
    url(r'^login',views.login),
    url(r'^introduction',views.introduction),
    url(r'^hotel',views.hotel),
    url(r'^shares',views.share),
]
