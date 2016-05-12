from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.colors import pink, black, red, blue, green, gray, Color
from reportlab.lib.pagesizes import letter
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from datetime import datetime
import math
from .reportlabs import *

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
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    types = Ticket.count_types(request.user)
    svalues = (UserProfile.get_UserProfile(request.user)).group_values(False)
    ivalues = (UserProfile.get_UserProfile(request.user)).group_values(True)
    rvalues = (UserProfile.get_UserProfile(request.user)).group_values(None)
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    activitiespop = Activity.pop(request.user)
    slaspop = Ticket.pop(request.user)
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/index.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/index.html'
        else:
            link ='TicketsApp/solver/index.html'
    return render(request, link, 
            {'userjob':userjob,'userdepartment':userdepartment,'psolicitude':psolicitude,'prequisite':prequisite,'grequisite':grequisite,
             'pincident':pincident,'gsolicitude':gsolicitude,'gincident':gincident,
             'svalues': svalues,'ivalues': ivalues,'rvalues': rvalues,'bvalues': types,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,'activitiespop':activitiespop,'slaspop':slaspop,
             })

@login_required(login_url ='')
def users(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    usershierarchy = request.user.profile.get_users_hierarchy()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/users_list.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/users_list.html'
        else:
            link ='TicketsApp/solver/users_list.html'
    return render(request, link, 
            {'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
             'gsolicitude':gsolicitude,'gincident':gincident,'prequisite':prequisite,'grequisite':grequisite,'servers': servers,
             'services' : services,'usershierarchy':usershierarchy,'notifications':notifications,
             })

def users_id(request,pk):
    userp= User.objects.get(pk=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    psolicitudea = Ticket.ticket_count_active(userp,False)
    pincidenta = Ticket.ticket_count_active(userp,True)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    ivalues = (UserProfile.get_UserProfile(request.user)).incident_group_values()
    bars = UserProfile.resume_in_time(userp,datetime.now()-timedelta(days=30),datetime.now())
    usershierarchy = request.user.profile.get_users_hierarchy()
    lastten = Activity.last_ten_of_user(userp)
    usertickets = Ticket.objects.filter(t_usersolver=userp)
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/users_id.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/users_id.html'
        else:
            link ='TicketsApp/solver/users_id.html'
    return render(request, link, 
            {'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
             'psolicitudea':psolicitudea,'pincidenta':pincidenta,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
             'gincident':gincident,'servers': servers,'services' : services,'usershierarchy':usershierarchy,'userp':userp,
             'lastten':lastten,'usertickets':usertickets,'notifications':notifications,'bars':bars,'ivalues':ivalues,
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
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    psolicitudes = Ticket.tickets(request.user,True,False)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/personal_solicitude.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/personal_solicitude.html'
        else:
            link ='TicketsApp/solver/personal_solicitude.html'
    return render(request, link, {'userjob':userjob,
             'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
             'gincident':gincident,'psolicitudes':psolicitudes,'servers':servers,
             'services':services,'notifications':notifications,
                 })

def solicitudg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    gsolicitudes = Ticket.tickets(request.user,False,False)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/group_solicitude.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/group_solicitude.html'
        else:
            link ='TicketsApp/solver/group_solicitude.html'
    return render(request, link,{'userjob':userjob,
             'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
             'gincident':gincident,'gsolicitudes':gsolicitudes,'servers':servers,
             'services':services,'notifications':notifications,
                 })
   
def incidentp(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    pincidents = Ticket.tickets(request.user,True,True)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/personal_incidents.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/personal_incidents.html'
        else:
            link ='TicketsApp/solver/personal_incidents.html'
    return render(request, link, {'userjob':userjob,
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
         'gincident':gincident,'pincidents':pincidents,'servers':servers,
         'services':services,'notifications':notifications,
             })

def incidentg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    gincidents = Ticket.tickets(request.user,False,True)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/group_incidents.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/group_incidents.html'
        else:
            link ='TicketsApp/solver/group_incidents.html'
    return render(request, link, {'userjob':userjob,
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
         'gincident':gincident,'gincidents':gincidents,'servers':servers,
         'services':services,'notifications':notifications,
             })

def requisitep(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    prequisites = Ticket.tickets(request.user,True,None)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/personal_requisites.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/personal_requisites.html'
        else:
            link ='TicketsApp/solver/personal_requisites.html'
    return render(request, link, {'userjob':userjob,
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
         'gincident':gincident,'prequisites':prequisites,'servers':servers,
         'services':services,'notifications':notifications,
             })

def requisiteg(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    grequisites = Ticket.tickets(request.user,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/group_requisites.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/group_requisites.html'
        else:
            link ='TicketsApp/solver/group_requisites.html'
    return render(request, link, {'userjob':userjob,
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
         'gincident':gincident,'grequisites':grequisites,'servers':servers,
         'services':services,'notifications':notifications,
             })

def ptasks(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    ptasks = Ticket.tasks(request.user)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    link = ''
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/tasks.html'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/tasks.html'
        else:
            link ='TicketsApp/solver/tasks.html'
    return render(request, link, {'userjob':userjob,
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,'prequisite':prequisite,'grequisite':grequisite,
         'gincident':gincident,'ptasks':ptasks,'servers':servers,
         'services':services,
         'notifications':notifications,
             })

def ticket(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    try:
        ticketpk = Ticket.objects.get(pk=pk)
    except:
        ticketpk = None
    if ticketpk :
        if (ticketpk.t_viewers.find(request.user.username)==-1):
            ticketpk.t_viewers += request.user.username+","
            ticketpk.save()
        useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
        usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
        sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
        slahour = sla.seconds//3600
        slaminute = (sla.seconds //60)%60
        attacheds = Archive.archives_of_a_ticket(ticketpk)
        sons = Ticket.get_sons(ticketpk)
        activities = Activity.activities_of_a_ticket(ticketpk)
        for activity in activities:
            if (activity.at_viewers.find(request.user.username)==-1):
                activity.at_viewers += request.user.username+","
                activity.save()
        lastactivity = Activity.last_modified(ticketpk)
        dateopen = Activity.date_of_event(ticketpk,'')
        datesolved = Activity.date_of_event(ticketpk,'Resuelto')
        dateclosed = Activity.date_of_event(ticketpk,'Cerrado')
        link = ''
        if (userdepartment.leader_of_department() == request.user):
            link = 'TicketsApp/leader/ticketid.html'
        else:
            if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
                link ='TicketsApp/creator/ticketid.html'
            else:
                link ='TicketsApp/solver/ticketid.html'
        return render(request,link,{
             'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
             'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
            'services':services,'dateopen':dateopen,'notifications':notifications,
             })
    else: return render(request,'TicketsApp/page_404.html')

def ticket_create(request,pk):
    if (pk == 'solicitud'):
        isincident = False
    else:
        if (pk == 'requisito'):
            isincident = None
        else:
            isincident = True
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    usersofdep = Department.from_user_get_depusers(request.user)
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if request.method =="POST":
        formTicket = CreateTicketForm(request.POST)
        ticketpk = formTicket.save(commit=False)
        ticketpk.t_userreporter = request.user
        ticketpk.t_state = "Iniciado"
        ticketpk.t_isincident = isincident    
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
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
        'gsolicitude':gsolicitude,'gincident':gincident,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
        'isincident':isincident,
             })
    
def ticket_edit(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
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
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if (userdepartment.leader_of_department() == request.user):
        link = 'TicketsApp/leader/'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/'
        else:
            link ='TicketsApp/solver/'
    if request.method =="POST":
        formTicket = EditTicketStateForm(request.POST, instance = ticketpk)
        newactivity = Activity.insert(ticketpk,
            request.POST.get('t_state'),
            request.user,datetime.now(),
            "El estado ha sido cambiado de "+ticketpk.t_state+" a "+request.POST.get('t_state'))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.usersolver=request.user
        ticketpk.save()
        return render(request, link+'ticketid.html',{
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
        'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
        'services':services,'notifications':notifications,
         })
    else:
        formTicket = EditTicketStateForm(instance=ticketpk)
        return render(request,link+'ticketid_edit.html',{
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
        'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
         })

def ticket_attach(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
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
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if (userdepartment.leader_of_department() == request.user):
            link = 'TicketsApp/leader/'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/'
        else:
            link ='TicketsApp/solver/'  
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
        return render(request,link+'ticketid.html',{
         'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
         'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
        'services':services,'archiveattached':archiveattached,'notifications':notifications,
         })
    else:
        formArchive = AddArchiveForm(instance=ticketpk)
        return render(request,link+'ticketid_attach.html',{
         'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
         'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
        'services':services,'usersofdep':usersofdep,'formArchive':formArchive,'notifications':notifications,
         })

def ticket_scale(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
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
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if (userdepartment.leader_of_department() == request.user):
            link = 'TicketsApp/leader/'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/'
        else:
            link ='TicketsApp/solver/'  
    if request.method =="POST":
        formTicket = EditScaleForm(request.POST, instance = ticketpk)
        newactivity = Activity.insert(ticketpk,
            "Escalamiento",
            request.user,datetime.now(),
            "El ticket ha sido escalado de prioridad "+str(ticketpk.t_priority)+" a prioridad "+str(request.POST.get('t_priority')))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.save()
        return render(request,link+'ticketid.html',{
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
        'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
        'services':services,'notifications':notifications,
         })
    else:
        formTicket = EditScaleForm(instance=ticketpk)
        return render(request,link+'ticketid_scale.html',{
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
        'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
         }) 

def ticket_transfer(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
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
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if (userdepartment.leader_of_department() == request.user):
            link = 'TicketsApp/leader/'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/'
        else:
            link ='TicketsApp/solver/'  
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
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
            'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
            'services':services,'notifications':notifications,
             })
    else:
        formTicket = TransferForm(instance=ticketpk)
        return render(request,'TicketsApp/creator/ticketid_transfer.html',{
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
            'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
            'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
             })
    
def ticket_assign(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
    prequisite = Ticket.ticket_count(request.user,True,None)
    grequisite = Ticket.ticket_count(request.user,False,None)
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
    notifications = Ticket.objects.filter(t_department=request.user.profile.u_department,t_state="Iniciado").order_by('-t_reportmadeon')[:8]
    if (userdepartment.leader_of_department() == request.user):
            link = 'TicketsApp/leader/'
    else:
        if (UserProfile.get_UserProfile(request.user).u_cancreatetickets) :
            link ='TicketsApp/creator/'
        else:
            link ='TicketsApp/solver/'  
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
        return render(request,link+'ticketid.html',{
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
            'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
            'services':services,'notifications':notifications,
                 })
    else:
        formTicket = AsignateSolverTicketForm(instance=ticketpk)
        formTicket.fields['t_usersolver'].queryset = UserProfile.get_users_hierarchy(request.user.profile)
        return render(request,link+'ticketid_assign.html',{
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,'prequisite':prequisite,'grequisite':grequisite,
            'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
            'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
                 })

def ticket_print(request,pk):
    return ticket_printed(request,pk)

def ticket_close(request,pk):
    ticketpk = Ticket.objects.get(pk=pk)
    ticketpk.t_issolved = True
    ticketpk.t_state = "Cerrado"
    link ='TicketsApp/creator/'
    newactivity = Activity.insert(ticketpk,
            "Cerrado",
            request.user,
            datetime.now(),
            "El ticket ha sido Cerrado por "+str(request.user.get_full_name()) +" \n")
    newactivity.save()
    ticketpk.save()
    return redirect(reverse('index'))