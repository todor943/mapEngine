from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ApiView.as_view(), name='root'),
    # url(r'^$', views.ApiView.as_view(), name='getEvents'),
    # url(r'^$', views.ApiView.as_view(), name='updateUser  ')
]
