from django.contrib.auth import login
from django.shortcuts import redirect, render
from users.forms import CustomUserCreationForm
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib import messages

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.is_staff = True
            user.save()
            permission_list = ['view_depot','view_courier','view_client',
                                'add_depot','add_courier','add_client',
                                'change_depot','change_courier','change_client',
                                'delete_depot','delete_courier','delete_client']
            permission_list = list(map(lambda x : Permission.objects.get(codename=x), permission_list))
            user.user_permissions.add(*permission_list)
            login(request, user)
            return redirect('/admin/')
        else:
            messages.info(request, 'There is something wrong with your registration. Please try again!')
            return redirect(reverse('register'))