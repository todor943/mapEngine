import datetime
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField, GeoManager
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Model, CharField, ForeignKey,\
    TextField, DateTimeField, UUIDField, CASCADE, OneToOneField
from django.dispatch import receiver
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from MapApi import signals


# Create your models here.
class EventType(Model):
    name = CharField(null=False, max_length=30)

    def __str__(self):
        return str(self.name)

class MapEntity(Model):
    
    # entityName = CharField(max_length=60, help_text="Insert name here")
    entityType = CharField(max_length=60, help_text="Insert name here")
    # entityType = ForeignKey(EventType, help_text="What type of event is it?")

    # entityDescription = TextField(max_length=300, help_text="Very awesome party at my place")
    owner = ForeignKey(User, on_delete=CASCADE)
    publishDate = DateTimeField(null=False, auto_now_add=True)
    # lastModDate = DateTimeField(null=True, auto_now=True)

    # uuid = UUIDField(default=uuid.uuid4, editable=False)

    geoLocationField = PointField(srid=4326)
    objects = GeoManager()

    def setLocationField(self, lat, lng) :
        self.geoLocationField = GEOSGeometry('POINT(' + str(lng)  + ' '+ str(lat)  + ')', srid=4326)

    # json encode maybe?!
    def __str__(self):
        return str(self.entityType + ":::" + str(self.geoLocationField))


class Player(Model):
    user = OneToOneField(User)
    lastLocation = PointField(srid=4326)
    objects = GeoManager()
