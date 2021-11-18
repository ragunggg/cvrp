from django.conf.urls import url
from cvrp.views import Clients_view

app_name = 'cvrp'
urlpatterns = [
    url(r"^", Clients_view, name="clients_view"),
]