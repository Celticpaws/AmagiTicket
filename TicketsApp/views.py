from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from .models import *
from .forms import *
from datetime import datetime


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
    types = Ticket.count_types(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    return render(request, 'TicketsApp/index.html', 
        {'userjob':userjob,
         'psolicitude':psolicitude,
         'pincident':pincident,
         'gsolicitude':gsolicitude,
         'gincident':gincident,
         'svalues': [[request.user, psolicitude], [userdepartment, gsolicitude-psolicitude]],
         'ivalues': [[request.user, pincident], [userdepartment, gincident-pincident]],
         'bvalues': types,
         'servers': servers,
         'services' : services
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
    servers = Server.server_count()
    services = Service.service_count()
    return render(request, 'TicketsApp/personal_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'psolicitudes':psolicitudes,         'servers':servers,
         'services':services,
         })

def solicitudg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    gsolicitudes = Ticket.group_solicitudes(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    return render(request, 'TicketsApp/group_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'gsolicitudes':gsolicitudes,         'servers':servers,
         'services':services,
         })

def incidentp(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    pincidents = Ticket.personal_incidents(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    return render(request, 'TicketsApp/personal_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'pincidents':pincidents,         'servers':servers,
         'services':services,
         })

def incidentg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    gincidents = Ticket.group_incidents(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    return render(request, 'TicketsApp/group_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'gincidents':gincidents,         'servers':servers,
         'services':services,
         })

def ticket(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    ticketpk = Ticket.objects.get(pk=pk)
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = ticketpk.t_sla-timezone.now()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk)
    lastactivity = Activity.last_modified(ticketpk)
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
    return render(request,'TicketsApp/ticketid.html',{
         'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
         'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
        'services':services,})

def ticket_edit(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    ticketpk = Ticket.objects.get(pk=pk)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = ticketpk.t_sla-timezone.now()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk)
    lastactivity = Activity.last_modified(ticketpk)
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
    usersofdep = Department.from_user_get_depusers(request.user)
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    if request.method =="POST":
        formTicket = EditTicketStateForm(request.POST, instance = ticketpk)
        newactivity = Activity.insert(ticketpk,
            "Cambio de estado",
            request.user,datetime.now(),
            "El estado ha sido cambiado de "+ticketpk.t_state+" a "+request.POST.get('t_state'))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.usersolver=request.user
        ticketpk.save()
        return render(request,'TicketsApp/ticketid.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
        'services':services,})
    else:
        formTicket = EditTicketStateForm(instance=ticketpk)
    return render(request,'TicketsApp/ticketid_edit.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
        'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})


def ticket_attach(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    ticketpk = Ticket.objects.get(pk=pk)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = ticketpk.t_sla-timezone.now()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk)
    lastactivity = Activity.last_modified(ticketpk)
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
    usersofdep = Department.from_user_get_depusers(request.user)
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    if request.method =="POST":
        formArchive = AddArchiveForm(request.POST,request.FILES)
        newactivity = Activity.insert(ticketpk,
            "Archivo adjunto",
            request.user,datetime.now(),
            "Se ha adjuntado el archivo "+request.POST.get('a_name'))
        archiveattached = Archive.insert(ticketpk,
            request.POST.get('a_name'),
            request.FILES['a_route'],
            request.POST.get('a_description'),
            datetime.now(),
            request.user)
        archiveattached.save()
        newactivity.save()
        return render(request,'TicketsApp/ticketid.html',{
         'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
         'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
        'services':services,        'archiveattached':archiveattached,})
    else:
        formArchive = AddArchiveForm(instance=ticketpk)
    return render(request,'TicketsApp/ticketid_attach.html',{
         'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
         'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
        'services':services,        'usersofdep':usersofdep,        'formArchive':formArchive,})


def ticket_scale(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    ticketpk = Ticket.objects.get(pk=pk)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = ticketpk.t_sla-timezone.now()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk)
    lastactivity = Activity.last_modified(ticketpk)
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
    usersofdep = Department.from_user_get_depusers(request.user)
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    if request.method =="POST":
        formTicket = EditScaleForm(request.POST, instance = ticketpk)
        newactivity = Activity.insert(ticketpk,
            "Escalamiento",
            request.user,datetime.now(),
            "El ticket ha sido escalado de prioridad "+str(ticketpk.t_priority)+" a prioridad"+str(request.POST.get('t_priority')))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.save()
        return render(request,'TicketsApp/ticketid.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
        'services':services,})
    else:
        formTicket = EditScaleForm(instance=ticketpk)
    return render(request,'TicketsApp/ticketid_scale.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
        'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})


