from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.serializers import CharField, FloatField, IntegerField, DateTimeField, Serializer
from rest_framework.serializers import UUIDField
from rest_framework_gis.serializers import GeometryField
import uuid

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import MapApp
import pprint

class MapEntitySerializer(Serializer):
    """ A class to serialize locations as GeoJSON compatible data """

    entityType = CharField(max_length=20, help_text="Insert type here")
    # geoLocationField = GeometryField(srid=4326)
    # insert hacks 
    internal_request = None
    owner = None

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
                
        validated_data['owner_id'] = self.owner.id
        m_ent = MapApp.models.MapEntity(**validated_data)
        m_ent.owner = self.owner

        m_ent.setLocationField(self.internal_request._data['lat']\
            ,self.internal_request._data['lng'])
        m_ent.save()
        # pprint.pprint(self.internal_request.__dict__)
        pprint.pprint(m_ent.__dict__)
        return m_ent
        # return MapApp.models.MapEntity.objects.create(**validated_data)

    def update(self,  instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        print(instance) 
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        instance.owner = user
        # instance.setLocationField(self.lat, self.lng)
        instance.entityName = "TEST"
        instance.entityType = "test"
        instance.entityDescription = "test"
        
        # lat = validated_data.get('lat', instance.lat)
        # instance.lng = validated_data.get('lng', instance.lat)

        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)
        # instance.save()
        # return {}
        return instance

class EventQuery(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    serializer_classes = (MapEntitySerializer,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        
        return Response([str(123)])

    def post(self, request, format=None):
        serializer = MapEntitySerializer(data=request.data)

        user = None
        if request and hasattr(request, "user"):
            user = request.user
        serializer.owner = user
        serializer.internal_request = request

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

