from django.shortcuts import *
from django.core import *
from django.http import *
from django.views.generic import *
from django.contrib.gis.serializers import geojson
from django.contrib.gis.geos import GEOSGeometry
import pprint
import time

from django.contrib.auth.decorators import *
from django.contrib.auth import *
import json
from .models import *
import MapApp


class ApiView(View):
    def get(self, request):
        data = serializers.serialize("geojson", MapApp.models.MapEntity.objects.all())
        return HttpResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}

        if request.user.is_authenticated():
            requestData = json.loads(request.POST['jsonData'])
            now = time.time()
            request.session['location'] = requestData['position']
            request.session['mapOptions'] = requestData['mapOptions']
            request.session['lastUpdate'] = time.time()
            radius = requestData['radius']
            searchPnt = self.locationToPoint(requestData['position']);
            data =  MapApp.models.MapEntity.objects.filter(geoLocationField__distance_lte=(searchPnt, radius))
            data = serializers.serialize("geojson", data)
            print "Updated the user's map state in session"
        # print request.user.get_username()
        return HttpResponse(data)

    def locationToPoint(self, position):
        return GEOSGeometry('POINT(' + str(position['lng'])  + ' '+ str(position['lat'])  + ')', srid=4326)

    def handleRequest(self, request):
        pass


    def getEventsInRadius(self, centerPnt, distance):
        pass

    def updateSession(self, request):
        pass

class EventQuery(View):
    def get(self, request):
        return HttpResponse("123");


    def post(self, request):
        return HttpResponse("123");
