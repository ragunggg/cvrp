from django.conf.urls import url
from cvrp.views import Clients_view

urlpatterns = [
    url(r"^", Clients_view, name="client_view"),
]