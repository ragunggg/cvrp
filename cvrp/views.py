from django.shortcuts import render
from cvrp.models import Client
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
@csrf_exempt
def Clients_view(request):
    username = request.user.username
    if request.method == 'POST': 
        clients_name  = request.POST.getlist('clients_name')
        return HttpResponse(clients_name)
    else:
        clients = Client.objects.filter(user__username=username)
        context = {
        'clients': clients
        }

    return render(request, 'cvrp/render_client.html', context)