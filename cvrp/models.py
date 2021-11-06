from django.contrib.gis.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Depot(models.Model):
    name = models.CharField(_('Depot Name'), max_length=100)
    address = models.CharField(_('Depot Address'), max_length=100, blank=True)
    location = models.PointField(_('Depot Location'))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


class Courier(models.Model):
    name = models.CharField(_('Courier Name'), max_length=100)
    capacity = models.PositiveIntegerField(_('Courier Capacity'))
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(_('Client Name'), max_length=100)
    address = models.CharField(_('Client Address'), max_length=100, blank=True)
    demand = models.PositiveIntegerField(_('Client Demand'))
    location = models.PointField(_('Client Location'))
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name
