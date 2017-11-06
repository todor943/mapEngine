import json
import pprint
import time

from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.hashers import make_password
# from .models import *
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.gis.serializers import geojson
from django.core import *
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *
from django.utils.decorators import *
from django.views.generic import *
from rest_framework.authtoken.models import Token

from MapApp.forms import *
from MapApp.models import *

from django.conf import settings
from MapApi import signals
from django.dispatch import receiver


class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            f = LoginForm()
            context = {'form':f}
            return render(request, 'registration/login.html', context)
        else:
            return redirect('index')
    
    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def post(self, request):
        f = LoginForm(request.POST or None)
        if f.is_valid():
            user = authenticate(request, \
                username = f.cleaned_data['username'], \
                password = f.cleaned_data['password'])
            if user is not None :
                login(request, user)
                signals.user_login.send(sender=None, request=request, user=request.user)
                
        # usn = request.POST['username']
        # psw = request.POST['password']
        # # psw = make_password(psw)
        # user = authenticate(request, username=usn, password=psw)
        # if user is not None:
        #     login(request, user)
        return redirect('index')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

    def post(self, request):
        logout(request)
        return redirect('index')

@method_decorator(login_required, name='dispatch')
class MapView(View):
    def get(self, request):
        # pprint.pprint(reverse('map'))
        if request.user.is_authenticated():
            tokenUser = request.user
            token = Token.objects.get(user=tokenUser)
            # token.key
        return render(request, 'MapApp/map.html', {
            "authToken" : token.key
        })


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        context = {'var' : 123}
        return render(request, 'index.html', context)



# @method_decorator(login_required, name='dispatch')
# class NewEventView(View):
#     def get(self, request):
#         context = {}
#         f = EventForm();
#         context = {'form':f, 'apiUrl' : '/api/'}
#         opts = request.session.get('mapOptions', None)
#         if opts is not None:
#             context['mapOptions'] = json.dumps(opts)
#         return render(request, 'MapApp/newEvent.html', context)


#     def post(self, request):
#         context = {}
#         f = EventForm(request.POST or None)
#         context = {'form':f, 'apiUrl' : '/api/'}
#         opts = request.session.get('mapOptions', None)
#         if opts is not None:
#             context['mapOptions'] = json.dumps(opts)
#         if f.is_valid():
#             ment = f.save(commit=False)
#             ment.setLocationField(lat=request.POST['locLat'], lng= request.POST['locLong'])
#             ment.owner = request.user
#             ment.save()
#             pprint.pprint(ment)
#             return redirect('map')
#         return render(request, 'MapApp/newEvent.html', context)


class RegisterView(AbstractUser, View):
    def get(self, request):
        if request.user.is_authenticated():
            redirect('map');
        context = {}
        f = RegisterForm();
        context = {'form':f}
        return render(request, 'registration/register.html', context)


    def post(self, request):
        if request.user.is_authenticated():
            redirect('map');
        context = {}
        f = RegisterForm(request.POST or None)
        context = {'form':f}

        if f.is_valid():
            userInstance = f.save()
            Token.objects.create(user=userInstance)
            pprint.pprint('valid user making')
            login(request, userInstance)
            return redirect('map')

        return render(request, 'registration/register.html', context)


@method_decorator(login_required, name='dispatch')
class MyEvents(View):
    def get(self, request):
        objectList = MapEntity.objects.filter(owner=request.user)
        context = {'events' : objectList}
        pprint.pprint(objectList[0])
        return render(request, 'MapApp/listEvents.html', context)


@method_decorator(login_required, name='dispatch')
class EventDetail(View):
    def get(self, request):
        pass
