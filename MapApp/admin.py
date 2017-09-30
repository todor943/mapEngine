from django.contrib import admin

from .models import EventType, MapEntity, Player


admin.site.register(MapEntity)
admin.site.register(EventType)
admin.site.register(Player)
