from django.shortcuts import *
from django.core import *
from django.http import *
from django.views.generic import *
from django.contrib.gis.serializers import geojson
import pprint
import time

from django.contrib.auth.decorators import *
from django.contrib.auth import *
from django.utils.decorators import *
from django.core.urlresolvers import reverse
import json
from .forms import *
from .models import *

class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            f = LoginForm()
            context = {'form':f}
            return render(request, 'registration/login.html', context)
        else:
            return redirect('index')

    def post(self, request):
        usn = request.POST['username']
        psw = request.POST['password']
        user = authenticate(username=usn, password=psw)
        if user is not None:
            login(request, user)
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
        return render(request, 'MapApp/map.html')


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        context = {'var' : 123}
        return render(request, 'index.html', context)



@method_decorator(login_required, name='dispatch')
class NewEventView(View):
    def get(self, request):
        context = {}
        f = EventForm();
        context = {'form':f, 'apiUrl' : '/api/'}
        opts = request.session.get('mapOptions', None)
        if opts is not None:
            context['mapOptions'] = json.dumps(opts)
        return render(request, 'MapApp/newEvent.html', context)


    def post(self, request):
        context = {}
        f = EventForm(request.POST or None)
        context = {'form':f, 'apiUrl' : '/api/'}
        opts = request.session.get('mapOptions', None)
        if opts is not None:
            context['mapOptions'] = json.dumps(opts)
        if f.is_valid():
            ment = f.save(commit=False)
            ment.setLocationField(lat=request.POST['locLat'], lng= request.POST['locLong'])
            ment.owner = request.user
            ment.save()
            pprint.pprint(ment)
            return redirect('map')
        return render(request, 'MapApp/newEvent.html', context)


class RegisterView(View):
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
            f.save()
            userInstance = f.save(commit=False)
            userInstance.backend = 'django.contrib.auth.backends.ModelBackend'
            userInstance.save()
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
