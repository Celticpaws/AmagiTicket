from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from .models import *


# Create your views here.
#def auth(request):
#	users = UserProfile.objects.filter(u_createddate__lte=timezone.now()).order_by('u_createddate')
#	return render(request, 'TicketsApp/auth.html', {'users': users})


@login_required(login_url ='')
def index(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    return render(request, 'TicketsApp/index.html', 
        {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'svalues': [[request.user, psolicitude], [userdepartment, gsolicitude-psolicitude]],
         'ivalues': [[request.user, pincident], [userdepartment, gincident-pincident]],
         })

def auth(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
                # Lo dejo como ejercicio al lector :)
                pass
        mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request, 'TicketsApp/auth.html', {'mensaje': mensaje})

@login_required(login_url ='')
def main(request):
	return render(request, 'TicketsApp/main.html', {})

def register(request):
	return render(request, 'TicketsApp/register.html', {})

def solicitudp(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    psolicitudes = Ticket.personal_solicitudes(request.user)
    return render(request, 'TicketsApp/personal_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'psolicitudes':psolicitudes,
         })

def solicitudg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    gsolicitudes = Ticket.group_solicitudes(request.user)
    return render(request, 'TicketsApp/group_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'gsolicitudes':gsolicitudes,
         })

def incidentp(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    pincidents = Ticket.personal_incidents(request.user)
    return render(request, 'TicketsApp/personal_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'pincidents':pincidents,
         })

def incidentg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    gincidents = Ticket.group_incidents(request.user)
    return render(request, 'TicketsApp/group_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'gincidents':gincidents,
         })

def ticket(request,pk):
    ticketpk = Ticket.objects.get(pk=pk)
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    return render(request,'TicketsApp/ticketid.html',{'ticketpk':ticketpk,'useraffected':useraffected})


