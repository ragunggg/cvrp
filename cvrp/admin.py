from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Depot, Courier, Client

@admin.register(Depot)
class DepotAdmin(LeafletGeoAdmin):
    list_display = ['name', 'address']

@admin.register(Courier)
class CourierAdmin(LeafletGeoAdmin):
    list_display = ['name', 'capacity']

@admin.register(Client)
class ClientAdmin(LeafletGeoAdmin):
    list_display = ['name', 'address', 'demand']