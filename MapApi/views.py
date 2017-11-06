import json
import pprint
import time
import datetime
import django.core.serializers
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.serializers import geojson
from django.core import *
from django.http import *
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer,GeoFeatureModelListSerializer 
from rest_framework_gis.serializers import ListSerializer, ModelSerializer
from rest_framework.serializers import Serializer, FloatField, CharField
from rest_framework.serializers import DecimalField, IntegerField, DateTimeField
from rest_framework.response import Response
from rest_framework.views import APIView

import MapApp


class FakeApiView(View):
	def get(self, request):
		time_filter = datetime.datetime.now() - datetime.timedelta(minutes = 60)
		# data = django.core.serializers.serialize(
		# 	"geojson", MapApp.models.MapEntity.objects.all()
		# )
		data = django.core.serializers.serialize(
			"geojson", MapApp.models.MapEntity.objects.filter(
				publishDate__gte=time_filter
			)
		)
		return HttpResponse(data)

	def post(self, request, *args, **kwargs):
		data = {}

		if request.user.is_authenticated():
			requestData = json.loads(request.POST['jsonData'])
			now = time.time()
			if 'position' not in requestData:
				return JsonResponse({})
			request.session['location'] = requestData['position']
			request.session['mapOptions'] = requestData['mapOptions']
			request.session['lastUpdate'] = time.time()
			radius = requestData['radius']
			searchPnt = self.locationToPoint(requestData['position']);
			data =  MapApp.models.MapEntity.objects.filter(geoLocationField__distance_lte=(searchPnt, radius))
			data = django.core.serializers.serialize("geojson", data)
			print ("Updated the user's map state in session")
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


class ObtainAuthToken(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthTokenSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		# Token.objects
		
		# token, created = Token.objects.create(user=user)
		doDelete = True
		try:
			currentToken = Token.objects.get(user=user)
		# TODO 
		except Exception:
			doDelete = False

		if doDelete:
			print("Renewing user token")
			currentToken.delete()
		else :
			print("Attempting to create new user token")

		token = Token.objects.create(user=user)

		return Response({'token': token.key})
	

