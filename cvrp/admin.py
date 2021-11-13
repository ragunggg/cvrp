from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from django import forms
from .models import *

@admin.register(Depot)
class DepotAdmin(LeafletGeoAdmin):
    list_display = ['name', 'address']
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(DepotAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user = request.user.id)

@admin.register(Courier)
class CourierAdmin(LeafletGeoAdmin):
    list_display = ['name', 'capacity']
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(CourierAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user = request.user.id)

@admin.register(Client)
class ClientAdmin(LeafletGeoAdmin):
    list_display = ['name', 'address', 'demand']
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user = request.user.id)