from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User;
import datetime
from datetime import datetime
import uuid

# Create your models here.
class EventType(models.Model):
    name = models.CharField(null=False, max_length=30)

    def __str__(self):
        return str(self.name)

class MapEntity(models.Model):
    # Name and type are required
    # entityName = models.TextField(null=False)
    # entityType = models.TextField(null=False)


    entityName = models.CharField(max_length=60, help_text="Insert name here")
    entityType = models.ForeignKey(EventType, help_text="What type of event is it?")
    entityDescription = models.TextField(max_length=300, help_text="Very awesome party at my place")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # set the publish date on creation
    publishDate = models.DateTimeField(null=False, auto_now_add=True)

    # time markers for start/end -> can be edited prior to start time
    # startDate = models.DateTimeField(null=True, blank=False)
    # endDate = models.DateTimeField(null=True, blank=True)

    # auto update on last save
    lastModDate = models.DateTimeField(null=True, auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    # this has to be a proper GeoField
    # locLat = models.FloatField()
    # locLong = models.FloatField()
    # srid=4326 is compatible with google maps
    geoLocationField = models.PointField(srid=4326)
    objects = models.GeoManager()

    def setLocationField(self, lat, lng) :
        self.geoLocationField = GEOSGeometry('POINT(' + str(lng)  + ' '+ str(lat)  + ')', srid=4326)

    # json encode maybe?!
    def __str__(self):
        return str(self.entityName)


class Player(models.Model):
    user = models.OneToOneField(User)
    lastLocation = models.PointField(srid=4326)
    objects = models.GeoManager()
