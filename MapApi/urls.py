from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

from .rest import EventQuery
from . import views

urlpatterns = [
    url(r'^$', views.FakeApiView.as_view(), name='root'),
    url(r'event$', csrf_exempt(EventQuery.as_view()), name='event'), 
    # url(r'^auth/', obtain_auth_token),
    url(r'^auth/', csrf_exempt(views.ObtainAuthToken.as_view())),
    # url(r'event$', views.EventQuery.as_view(), name='event'),    
    # url(r'^$', views.ApiView.as_view(), name='getEvents'),
    # url(r'^$', views.ApiView.as_view(), name='updateUser  ')
]
