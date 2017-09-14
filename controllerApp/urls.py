from django.conf.urls import url

from controllerApp import dispacher
from . import views

app_name = 'controllerApp'




urlpatterns = [

    # test ajax
    url(r'^form/$', views.form, name='form'),
    # test ajax
    url(r'^form/sendQuery$', dispacher.translate, name='form'),
    # ex: /mlRadio/
    url(r'^$', views.index, name='index'),



]