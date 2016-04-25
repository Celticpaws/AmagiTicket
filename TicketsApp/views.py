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
def handler404(request):
    response = render_to_response('TicketsApp/page_404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('TicketsApp/page_500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



@login_required(login_url ='')
def index(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    types = Ticket.count_types(request.user)
    svalues = (UserProfile.get_UserProfile(request.user)).solicitude_group_values()
    ivalues = (UserProfile.get_UserProfile(request.user)).incident_group_values()
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    if (userdepartment.leader_of_department() == request.user):
        return render(request, 'TicketsApp/leader/index.html', 
            {'userjob':userjob,
             'psolicitude':psolicitude,
             'pincident':pincident,
             'gsolicitude':gsolicitude,
             'gincident':gincident,
             'svalues': svalues,
             'ivalues': ivalues,
             'bvalues': types,
             'servers': servers,
             'services' : services,
             'taskcount' : taskcount,
             })
    else:
        if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
            return render(request, 'TicketsApp/creator/index.html', 
                {'userjob':userjob,
                 'psolicitude':psolicitude,
                 'pincident':pincident,
                 'gsolicitude':gsolicitude,
                 'gincident':gincident,
                 'svalues': [[request.user, psolicitude], [userdepartment, gsolicitude-psolicitude]],
                 'ivalues': [[request.user, pincident], [userdepartment, gincident-pincident]],
                 'bvalues': types,
                 'servers': servers,
                 'services' : services,
                 'taskcount' : taskcount,
                 })
        else:
            return render(request, 'TicketsApp/solver/index.html', 
                {'userjob':userjob,
                 'psolicitude':psolicitude,
                 'pincident':pincident,
                 'gsolicitude':gsolicitude,
                 'gincident':gincident,
                 'svalues': [[request.user, psolicitude], [userdepartment, gsolicitude-psolicitude]],
                 'ivalues': [[request.user, pincident], [userdepartment, gincident-pincident]],
                 'bvalues': types,
                 'servers': servers,
                 'services' : services,
                 'taskcount' : taskcount,
                 })

@login_required(login_url ='')
def users(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    usershierarchy = request.user.profile.get_users_hierarchy()
    if (userdepartment.leader_of_department() == request.user):
        return render(request, 'TicketsApp/leader/users_list.html', 
            {'userjob':userjob,
             'psolicitude':psolicitude,
             'pincident':pincident,
             'gsolicitude':gsolicitude,
             'gincident':gincident,
             'servers': servers,
             'services' : services,
             'usershierarchy':usershierarchy,
             })
    else:
        if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
            return render(request, 'TicketsApp/creator/users_list.html', 
                {'userjob':userjob,
                 'psolicitude':psolicitude,
                 'pincident':pincident,
                 'gsolicitude':gsolicitude,
                 'gincident':gincident,
                 'servers': servers,
                 'services' : services,
                 'usershierarchy':usershierarchy,
                 })
        else:
            return render(request, 'TicketsApp/solver/users_list.html', 
                {'userjob':userjob,
                 'psolicitude':psolicitude,
                 'pincident':pincident,
                 'gsolicitude':gsolicitude,
                 'gincident':gincident,
                 'servers': servers,
                 'services' : services,
                 'usershierarchy':usershierarchy,
                 })

def users_id(request,pk):
    userp= User.objects.get(pk=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    psolicitudea = Ticket.personal_solicitude_count_active(userp)
    pincidenta = Ticket.personal_incident_count_active(userp)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    usershierarchy = request.user.profile.get_users_hierarchy()
    lastten = Activity.last_ten_of_user(userp)
    usertickets = Ticket.objects.filter(t_usersolver=userp)
    return render(request, 'TicketsApp/leader/users_id.html', 
            {'userjob':userjob,
             'psolicitude':psolicitude,
             'pincident':pincident,
             'psolicitudea':psolicitudea,
             'pincidenta':pincidenta,
             'gsolicitude':gsolicitude,
             'gincident':gincident,
             'servers': servers,
             'services' : services,
             'usershierarchy':usershierarchy,
             'userp':userp,
             'lastten':lastten,
             'usertickets':usertickets,
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        return render(request, 'TicketsApp/creator/personal_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'psolicitudes':psolicitudes,         'servers':servers,
         'services':services,
         })
    else:
        return render(request, 'TicketsApp/solver/personal_solicitude.html', {'userjob':userjob,
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        return render(request, 'TicketsApp/creator/group_solicitude.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'gsolicitudes':gsolicitudes,         'servers':servers,
         'services':services,
         })
    else:
        return render(request, 'TicketsApp/solver/group_solicitude.html', {'userjob':userjob,
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        return render(request, 'TicketsApp/creator/personal_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'pincidents':pincidents,         'servers':servers,
         'services':services,
         })
    else:
        return render(request, 'TicketsApp/solver/personal_incidents.html', {'userjob':userjob,
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        return render(request, 'TicketsApp/creator/group_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'gincidents':gincidents,         'servers':servers,
         'services':services,
         })
    else:
        return render(request, 'TicketsApp/solver/group_incidents.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'gincidents':gincidents,         'servers':servers,
         'services':services,
         })

def ptasks(request):
    userjob = UserProfile.get_jobtitle(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    ptasks = Ticket.tasks(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        return render(request, 'TicketsApp/creator/tasks.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'ptasks':ptasks,         'servers':servers,
         'services':services,
         })
    else:
        return render(request, 'TicketsApp/solver/tasks.html', {'userjob':userjob,
         'psolicitude':psolicitude,         'pincident':pincident,         'gsolicitude':gsolicitude,
         'gincident':gincident,         'ptasks':ptasks,         'servers':servers,
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
    try:
        ticketpk = Ticket.objects.get(pk=pk)
    except:
        ticketpk = None
    if ticketpk :
        useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
        usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
        sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
        slahour = sla.seconds//3600
        slaminute = (sla.seconds //60)%60
        attacheds = Archive.archives_of_a_ticket(ticketpk)
        sons = Ticket.get_sons(ticketpk)
        activities = Activity.activities_of_a_ticket(ticketpk)
        lastactivity = Activity.last_modified(ticketpk)
        dateopen = ticketpk.t_reportmadeon
        datesolved = Activity.date_of_event(ticketpk,'Resuelto')
        dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
        if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
            return render(request,'TicketsApp/creator/ticketid.html',{
             'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
             'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
            'services':services,    'dateopen':dateopen})
        else:
            return render(request,'TicketsApp/solver/ticketid.html',{
             'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
             'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
            'services':services,    'dateopen':dateopen})
    else: return render(request,'TicketsApp/page_404.html')

def ticket_create(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.personal_solicitude_count(request.user)
    gsolicitude = Ticket.group_solicitude_count(request.user)
    pincident = Ticket.personal_incident_count(request.user)
    gincident = Ticket.group_incident_count(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    usersofdep = Department.from_user_get_depusers(request.user)
    if request.method =="POST":
        formTicket = CreateTicketForm(request.POST)
        ticketpk = formTicket.save(commit=False)
        ticketpk.t_reporter = request.user
        ticketpk.t_state = "Iniciado"
        ticketpk.isincident = False
        ticketpk.t_reportmadeon = datetime.now()
        ticketpk.t_usersolver = None
        ticketpk.save()
        usersolver = UserProfile.get_UserProfile(request.user)
        
        attacheds = Archive.archives_of_a_ticket(ticketpk)
        sons = Ticket.get_sons(ticketpk)
        activities = Activity.activities_of_a_ticket(ticketpk)
        lastactivity = Activity.last_modified(ticketpk)
        datesolved = Activity.date_of_event(ticketpk,'Resuelto')
        dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
        useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)

        return redirect(reverse('index'))
    else:
        formTicket = CreateTicketForm()
        return render(request,'TicketsApp/creator/ticketid_create.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,       'servers':servers, 
        'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})
    



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
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
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
            return render(request,'TicketsApp/creator/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = EditTicketStateForm(instance=ticketpk)
        return render(request,'TicketsApp/creator/ticketid_edit.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
            'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})
    else:
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
            return render(request,'TicketsApp/solver/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = EditTicketStateForm(instance=ticketpk)
        return render(request,'TicketsApp/solver/ticketid_edit.html',{
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
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
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
            return render(request,'TicketsApp/creator/ticketid.html',{
             'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
             'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
            'services':services,        'archiveattached':archiveattached,})
        else:
            formArchive = AddArchiveForm(instance=ticketpk)
        return render(request,'TicketsApp/creator/ticketid_attach.html',{
             'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
             'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
            'services':services,        'usersofdep':usersofdep,        'formArchive':formArchive,})
    else:
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
            return render(request,'TicketsApp/solver/ticketid.html',{
             'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
             'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,
            'services':services,        'archiveattached':archiveattached,})
        else:
            formArchive = AddArchiveForm(instance=ticketpk)
        return render(request,'TicketsApp/solver/ticketid_attach.html',{
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
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        if request.method =="POST":
            formTicket = EditScaleForm(request.POST, instance = ticketpk)
            newactivity = Activity.insert(ticketpk,
                "Escalamiento",
                request.user,datetime.now(),
                "El ticket ha sido escalado de prioridad "+str(ticketpk.t_priority)+" a prioridad "+str(request.POST.get('t_priority')))
            newactivity.save()
            ticketpk = formTicket.save(commit=False)
            ticketpk.save()
            return render(request,'TicketsApp/creator/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = EditScaleForm(instance=ticketpk)
        return render(request,'TicketsApp/creator/ticketid_scale.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
            'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})
    else:
        if request.method =="POST":
            formTicket = EditScaleForm(request.POST, instance = ticketpk)
            newactivity = Activity.insert(ticketpk,
                "Escalamiento",
                request.user,datetime.now(),
                "El ticket ha sido escalado de prioridad "+str(ticketpk.t_priority)+" a prioridad "+str(request.POST.get('t_priority')))
            newactivity.save()
            ticketpk = formTicket.save(commit=False)
            ticketpk.save()
            return render(request,'TicketsApp/solver/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = EditScaleForm(instance=ticketpk)
        return render(request,'TicketsApp/solver/ticketid_scale.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
            'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})

def ticket_transfer(request,pk):
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
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
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
    if UserProfile.get_UserProfile(request.user).u_cancreatetickets :
        if request.method =="POST":
            formActivity = TransferForm(request.POST, instance = ticketpk)
            newactivity = Activity.insert(ticketpk,
                "Transferencia",
                request.user,datetime.now(),
                "El ticket ha sido transferido de "+ticketpk.t_usersolver.get_full_name()+" a \'  \' \n a razon de: \n"+str(request.POST.get('at_description')))
            newactivity.save()
            ticketpk.t_usersolver = None
            ticketpk.t_department = UserProfile.get_department(ticketpk.t_userreporter)
            ticketpk.save()
            return render(request,'TicketsApp/creator/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = TransferForm(instance=ticketpk)
        return render(request,'TicketsApp/creator/ticketid_transfer.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
            'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})
    else:
        if request.method =="POST":
            formActivity = TransferForm(request.POST, instance = ticketpk)
            newactivity = Activity.insert(ticketpk,
                "Transferencia",
                request.user,datetime.now(),
                "El ticket ha sido transferido de "+ticketpk.t_usersolver.get_full_name()+" a \'  \' \n a razon de: \n"+str(request.POST.get('at_description')))
            newactivity.save()
            ticketpk.t_usersolver = None
            ticketpk.t_department = UserProfile.get_department(ticketpk.t_userreporter)
            ticketpk.save()
            return render(request,'TicketsApp/solver/ticketid.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
            'services':services,})
        else:
            formTicket = TransferForm(instance=ticketpk)
        return render(request,'TicketsApp/solver/ticketid_transfer.html',{
            'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
            'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
            'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
            'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
            'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
            'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
            'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})

def ticket_assign(request,pk):
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
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
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
        formActivity = AsignateSolverTicketForm(request.POST, instance = ticketpk)
        formActivity.fields['t_usersolver'].queryset = UserProfile.get_users_hierarchy(request.user.profile)
        if ticketpk.t_usersolver == None :
            newactivity = Activity.insert(ticketpk,
                "Asignado",
                request.user,datetime.now(),
                "El ticket ha sido asignado de \' \' a "+str(User.objects.get(pk=request.POST.get('t_usersolver')).get_full_name()) +" \n")
        else:
            newactivity = Activity.insert(ticketpk,
                "Asignado",
                request.user,datetime.now(),
                "El ticket ha sido asignado de "+ticketpk.t_usersolver.get_full_name()+" a "+str(User.objects.get(pk=request.POST.get('t_usersolver')).get_full_name()) +" \n")
        newactivity.save()
        ticketpk.t_usersolver = User.objects.get(pk=request.POST.get('t_usersolver'))
        ticketpk.t_department = UserProfile.get_department(request.POST.get('t_usersolver'))
        ticketpk.t_state = "Asignado"
        ticketpk.save()
        return render(request,'TicketsApp/creator/ticketid.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers,   
        'services':services,})
    else:
        formTicket = AsignateSolverTicketForm(instance=ticketpk)
        formTicket.fields['t_usersolver'].queryset = UserProfile.get_users_hierarchy(request.user.profile)
    return render(request,'TicketsApp/solver/ticketid_assign.html',{
        'userjob':userjob,         'psolicitude':psolicitude,         'pincident':pincident,
        'gsolicitude':gsolicitude,         'gincident':gincident,        'ticketpk':ticketpk,
        'useraffected':useraffected,        'usersolver':usersolver,        'sla':sla,
        'slahour':slahour,        'slaminute':slaminute,        'attacheds':attacheds,    
        'sons':sons,        'activities':activities,        'lastactivity':lastactivity,
        'datesolved':datesolved,        'dateclosed':dateclosed,        'servers':servers, 
        'services':services,        'usersofdep':usersofdep,        'formTicket':formTicket,})


