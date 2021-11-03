from django.urls import path
from cvrp import views

urlpatterns = [
    path('', views.cvrp, name='cvrp'),
]