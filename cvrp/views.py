from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from cvrp.models import Depot, Courier, Client
from cvrp import utils, maps
import osmnx as ox
import folium
import pickle
import os

script_dir = os.path.dirname(__file__)
rel_path = "data/G.obj"
abs_file_path = os.path.join(script_dir, rel_path)

north, east, south, west = -6.8606, 107.5534, -6.9660, 107.6602

with open(abs_file_path, 'rb') as f:
    G = pickle.load(f)

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
        name_list = [depot.name]+list(map(lambda x : x.name, clients_list))
        m = utils._plot_on_maps(latitude, longitude, name_list)
        distance = utils._distance_calculator(G,latitude,longitude)
        model_solver = utils.cvrp_solver(courier_count,courier_capacity,client_count,clients_demand,distance)
        solution = model_solver.run()
        if not solution:
            messages.info(request, 'Solution is Infeasible!')
            return redirect(reverse('cvrp:clients_view'))
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

    return render(request, 'cvrp/clients_view.html', context)