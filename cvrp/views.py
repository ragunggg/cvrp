from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cvrp.models import Depot, Courier, Client
from cvrp import utils, maps
import osmnx as ox
import folium

# Defining the map boundaries 
north, east, south, west = -6.8686, 107.636, -6.9181, 107.5862

# Extracting the map as a graph object 
G = ox.graph_from_bbox(north, south, east, west, network_type = 'drive',simplify=True) 

coordinates = [[north,west],
               [north,east],
               [south,east],
               [south,west],
               [north,west]]

bounding_PolyLine = folium.PolyLine(locations=coordinates,weight=5)

# Create your views here.
@login_required
@csrf_exempt
def Clients_view(request):
    username = request.user.username
    if request.method == 'POST': 
        clients_id  = request.POST.getlist('clients_id')
        clients_list = list(Client.objects.filter(pk__in=clients_id))
        clients_demand = [0]+list(map(lambda x : x.demand, clients_list))
        clients_latitude = list(map(lambda x : x.location[1], clients_list))
        clients_longitude = list(map(lambda x : x.location[0], clients_list))
        client_count = len(clients_list)+1
        couriers_list = list(Courier.objects.filter(user__username=username))
        couriers_name = list(map(lambda x : x.name, couriers_list))
        courier_capacity = list(map(lambda x : x.capacity, couriers_list))
        courier_count = len(couriers_list)
        depot = list(Depot.objects.filter(user__username=username))[0]
        depot_latitude = depot.location[1]
        depot_longitude = depot.location[0]
        latitude = [depot_latitude]+clients_latitude
        longitude = [depot_longitude]+clients_longitude
        m = utils._plot_on_maps(latitude, longitude)
        distance = utils._distance_calculator(G,latitude,longitude)
        model_solver = utils.cvrp_solver(courier_count,courier_capacity,client_count,clients_demand,distance)
        solution = model_solver.run()
        visual = utils.visualization(G,m,latitude,longitude,solution,couriers_name)
        visual_map = visual.cvrp_map()
        map_content = maps.html_template(visual_map,bounding_PolyLine)
        context = {
        'map_content': map_content._repr_html_()
        }
        return render(request, 'cvrp/map.html', context)

    else:
        clients = Client.objects.filter(user__username=username)
        context = {
        'clients': clients
        }

    return render(request, 'cvrp/render_client.html', context)