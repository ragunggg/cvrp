from django.shortcuts import render

# Create your views here.
def cvrp(request):
    return render(request, 'cvrp.html', {})