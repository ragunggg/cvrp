from django.shortcuts import render
from cvrp.models import Depot, Courier, Client
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
@csrf_exempt
def Clients_view(request):
    username = request.user.username
    if request.method == 'POST': 
        clients_list  = request.POST.getlist('clients_list')
        clients_demand = list(map(lambda x : x.demand, clients_list))
        clients_location = list(map(lambda x : x.location, clients_list))
        client_count = len(clients_list)
        couriers_list = list(Courier.objects.filter(user__username=username))
        courier_capacity = list(map(lambda x : x.capacity, couriers_list))
        courier_count = len(couriers_list)
        depot = list(Depot.objects.filter(user__username=username))[0]
        depot_location = depot.location

        return HttpResponse(clients_list)
    else:
        clients = Client.objects.filter(user__username=username)
        context = {
        'clients': clients
        }

    return render(request, 'cvrp/render_client.html', context)