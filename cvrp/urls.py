from django.conf.urls import url
from cvrp.views import Clients_view

urlpatterns = [
    url(r"^client/", Clients_view, name="client_view"),
]