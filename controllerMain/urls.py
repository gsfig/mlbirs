from django.conf.urls import url

from controllerMain import dispacher
from . import views

app_name = 'controllerMain'




urlpatterns = [

    # test ajax
    url(r'^form/$', views.form, name='form'),
    # test ajax
    url(r'^form/sendQuery$', dispacher.translate, name='form'),
    # ex: /mlRadio/
    url(r'^$', views.index, name='index'),



]