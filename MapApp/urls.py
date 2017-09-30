from django.conf.urls import url

from . import views
from .views import *

urlpatterns = [
    # url(r'^$', views.MapView.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='Ulogin'),
    url(r'^logout/$', views.LogoutView.as_view(), name='Ulogout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^manage/$', views.MyEvents.as_view(), name='manage'),
    url(r'^newEvent/$', views.NewEventView.as_view(), name='newEventUrl'),
]
