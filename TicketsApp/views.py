from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from datetime import datetime
import math

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
    types = Ticket.count_types(request.user)
    svalues = (UserProfile.get_UserProfile(request.user)).solicitude_group_values()
    ivalues = (UserProfile.get_UserProfile(request.user)).incident_group_values()
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
            {'userjob':userjob,'userdepartment':userdepartment,'psolicitude':psolicitude,
             'pincident':pincident,'gsolicitude':gsolicitude,'gincident':gincident,
             'svalues': svalues,'ivalues': ivalues,'bvalues': types,    
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
             'gsolicitude':gsolicitude,'gincident':gincident,'servers': servers,
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
    servers = Server.server_count()
    services = Service.service_count()
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
             'psolicitudea':psolicitudea,'pincidenta':pincidenta,'gsolicitude':gsolicitude,
             'gincident':gincident,'servers': servers,'services' : services,'usershierarchy':usershierarchy,'userp':userp,
             'lastten':lastten,'usertickets':usertickets,'notifications':notifications,
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
             'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,
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
             'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,
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
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,
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
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,
         'gincident':gincident,'gincidents':gincidents,'servers':servers,
         'services':services,'notifications':notifications,
             })

def ptasks(request):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
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
         'psolicitude':psolicitude,'pincident':pincident,'gsolicitude':gsolicitude,
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
             'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
        isincident = True
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    psolicitude = Ticket.ticket_count(request.user,True,False)
    gsolicitude = Ticket.ticket_count(request.user,False,False)
    pincident = Ticket.ticket_count(request.user,True,True)
    gincident = Ticket.ticket_count(request.user,False,True)
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
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
            "Cambio de estado",
            request.user,datetime.now(),
            "El estado ha sido cambiado de "+ticketpk.t_state+" a "+request.POST.get('t_state'))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.usersolver=request.user
        ticketpk.save()
        return render(request, link+'ticketid.html',{
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
        'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
         'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
         'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
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
            'userjob':userjob,'psolicitude':psolicitude,'pincident':pincident,
            'gsolicitude':gsolicitude,'gincident':gincident,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
            'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
                 })

def pageBrake(n):
    page = n/760
    return page

def ticket_print(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    try:
        ticketpk = Ticket.objects.get(pk=pk)
    except:
        ticketpk = None
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk).order_by('at_date')

    lastactivity = Activity.last_modified(ticketpk)
    dateopen = Activity.date_of_event(ticketpk,'')
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='Reporte-Ticket"+str(ticketpk.t_id)+".pdf'"

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,bottomup=0)
    p.setFont("Helvetica-Bold", 18)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(50, 50, "Reporte - Ticket #"+str(ticketpk.t_id))
    p.drawString(50, 60, "________________________________________________________")
    p.setFont("Helvetica", 14)
    p.drawString(50, 100, "Resumen del ticket")
    p.drawString(50, 105, "_______________________________________________________________")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, 125, "Titulo del ticket:")
    p.drawString(70, 149, "Fecha de resolución:")
    p.drawString(70, 173, "Ultima modificación: ")
    p.setFont("Helvetica", 10)
    p.drawString(80, 137, ticketpk.t_title)
    p.drawString(80, 161, datesolved)
    p.drawString(80, 185, lastactivity)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(300, 125, "Fecha de apertura:")
    p.drawString(300, 149, "Fecha de cierre:")
    p.setFont("Helvetica", 10)
    p.drawString(310, 137, dateopen)
    p.drawString(310, 161, dateclosed)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, 209,"Descripción: ")
    p.setFont("Helvetica", 10)
    textobject = p.beginText()
    textobject.setTextOrigin(75,221)
    textobject.setFont("Helvetica",10)
    j=0
    for line in ticketpk.t_description.split('\n') :
        if len(line)>90:
            i=0
            while i<len(line):
                if i+90 < len(line):
                    textobject.textLine(line[i:i+90])
                    i+=90
                else:
                    textobject.textLine(line[i:len(line)])
                    i = len(line)+1
            j+= len(line)/90
        else:
            textobject.textLine(line)
            j+=1
        if(pageBrake(j)>=1):
            p.showPage()
            j=20
    p.drawText(textobject)
    j= round(j)+1
    j = 233+12*j

    if(pageBrake(j)>=1):
        p.showPage()
        j=20

    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Detalle del Usuario Afectado")
    p.drawString(50, j+5, "_______________________________________________________________")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, j+25, "Gerencia:")
    p.drawString(70, j+49, "Departmento:")
    p.drawString(70, j+73, "Usuario final afectado: ")
    p.drawString(300, j+25, "Cuenta del usuario final afectado:")
    p.drawString(300, j+49, "Teléfono:")
    p.drawString(300, j+73, "Correo: ")
    p.setFont("Helvetica", 10)
    p.drawString(80, j+25+12, str(useraffected.u_management))
    p.drawString(80, j+49+12, str(useraffected.u_department))
    p.drawString(80, j+73+12, useraffected.u_user.get_full_name())
    p.drawString(310, j+25+12, str(useraffected.u_user.username))
    p.drawString(310, j+49+12, str(useraffected.u_phone))
    p.drawString(310, j+73+12, str(useraffected.u_user.email))

    j= j+73+36

    if(pageBrake(j)>=1):
        p.showPage()
        j=20

    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Detalle del Ticket")
    p.drawString(50, j+5, "_______________________________________________________________")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, j+25, "Tipo:")
    p.drawString(70, j+49, "Categoria:")
    p.drawString(70, j+73, "Servicio afectado: ")
    p.drawString(70, j+97, "Servidor afectado: ")

    p.drawString(240, j+25, "Prioridad:")
    p.drawString(240, j+49, "Estado actual: ")
    p.drawString(240, j+73, "Grupo solucionador:")
    p.drawString(240, j+97, "Usuario solucionador asignado:")
    
    p.drawString(420, j+25, "Ticket reportado por: ")
    p.drawString(420, j+49, "Impacto: ")
    p.drawString(420, j+73, "SLA:")
    p.drawString(420, j+97, "Tiempo de vida: ")

    p.setFont("Helvetica", 10)
    if ticketpk.t_isincident:
        p.drawString(80, j+25+12, "Incidente")
    else:
        p.drawString(80, j+25+12, "Solicitud")   
    p.drawString(80, j+49+12, ticketpk.t_category)
    p.drawString(80, j+73+12, str(ticketpk.t_server))
    p.drawString(80, j+97+12, str(ticketpk.t_service))

    p.drawString(250, j+25+12, str(ticketpk.t_priority))
    p.drawString(250, j+49+12, ticketpk.t_state)
    p.drawString(250, j+73+12, str(ticketpk.t_department))
    if ticketpk.t_usersolver == None :
        p.drawString(250, j+97+12, "El ticket no ha sido asignado")
    else:
        p.drawString(250, j+97+12, ticketpk.t_usersolver.get_full_name())

    p.drawString(430, j+25+12, ticketpk.t_userreporter.get_full_name())
    p.drawString(430, j+49+12, str(ticketpk.t_impact))
    p.drawString(430, j+73+12, str(ticketpk.t_sla))
    p.drawString(430, j+97+12, ticketpk.life_spawn()+str(j))
    j= j+97+36

    if(pageBrake(j)>=1):
        p.showPage()
        j=20

    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Actividades del ticket")
    p.drawString(50, j+5, "_______________________________________________________________")

    if len(activities) == 0:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "No hay actividades asociadas a este ticket ")
        j=j+25+24
    else:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "Tipo ")
        p.drawString(200, j+25, "Fecha")
        p.drawString(420, j+25, "Creada por")
        for activity in activities:
            p.setFont("Helvetica", 8)
            p.drawString(70, j+25+12, activity.at_tipe)
            p.drawString(200, j+25+12, activity.at_date.strftime("%d de %b del %Y a las %I:%M:%S %p"))
            p.drawString(420, j+25+12, activity.at_createdby.get_full_name())
            j = j+12
            if(pageBrake(j)>=1):
                p.showPage()
                j=20
        j=j+25+24
    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Detalle Padre/Hijo")
    p.drawString(50, j+5, "_______________________________________________________________")
    p.setFont("Helvetica-Bold", 10)
    if ticketpk.t_mother != None:
        p.drawString(70, j+25, "Padre: Ticket " + str(ticketpk.t_mother) )
        p.drawString(200, j+25,"Estado: "+ticketpk.t_mother.t_state)
        if ticketpk.t_mother.t_usersolver == None:
            p.drawString(350, j+25,"Asignatario: Ticket no asignado")
        else:
            p.drawString(350, j+25,"Asignatario: "+ticketpk.t_mother.t_usersolver.get_full_name())
    else:    
        p.drawString(70, j+25, "Padre: El ticket no posee padre" )
    j=j+12

    if len(sons) == 0:
        p.drawString(70, j+25, " El ticket no posee ningun hijo ")
        j=j+25+24
    else:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "Ticket hijo # ")
        p.drawString(150, j+25, " Fecha")
        p.drawString(300, j+25, "Estado")
        p.drawString(420, j+25, "Asigantatio")

        for son in sons:
            p.setFont("Helvetica", 8)
            p.drawString(80, j+25+12, str(son))
            p.drawString(150, j+25+12, son.t_reportmadeon.strftime("%d de %b del %Y a las %I:%M:%S %p"))
            p.drawString(300, j+25+12, son.t_state)
            if son.t_usersolver == None:
                p.drawString(420, j+25+12, "Ticket no asignado")
            else:
                p.drawString(420, j+25+12, son.t_usersolver.get_full_name()+str(j))
            j = j+12
            if(pageBrake(j)>=1):
                p.showPage()
                j=20
        j=j+25+24




    p.drawString(100,j,str(j))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response