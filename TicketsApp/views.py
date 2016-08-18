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
    dephierarchy = request.user.profile.from_level_get_dep()
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    types = []
    for ttype in ttypes:
        types += Ticket.count_types(request.user,dephierarchy,False,ttype)
    cake = []
    for ttype in ttypes:
        cake += [(UserProfile.get_UserProfile(request.user)).group_values(ttype)]
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    activitiespop = Activity.pop(request.user)
    slaspop = Ticket.pop(request.user)
    link ='TicketsApp/index.html'
    return render(request, link, 
            {'userjob':userjob,'userdepartment':userdepartment,
              #'psolicitude':psolicitude,'arequisite':arequisite,'prequisite':prequisite,'grequisite':grequisite,
             'dephierarchy':dephierarchy,
             'tctype':tctype,'cakes':cake,
             #'pincident':pincident,'gsolicitude':gsolicitude,'aincident':aincident,'asolicitude':asolicitude,'gincident':gincident,
             #'svalues': svalues,'ivalues': ivalues,'rvalues': rvalues,
             'bars': types,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,'activitiespop':activitiespop,'slaspop':slaspop,
             })

@login_required(login_url ='')
def departments(request):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    usershierarchy = request.user.profile.from_level_get_dep()
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link ='TicketsApp/departments_list.html'
    return render(request, link, 
            {'userjob':userjob,'dephierarchy':dephierarchy,'tctype':tctype,'servers': servers,
             'services' : services,'usershierarchy':usershierarchy,'notifications':notifications,
             })

def department_id(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userp= User.objects.get(pk=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    prequisite = Ticket.ticket_count(request.user,userdepartment,True,None)
    grequisite = Ticket.ticket_count_dep(request.user,dephierarchy,False,None)
    servers = Server.server_count()
    services = Service.service_count()
    types = Ticket.count_types(userp,userp.profile.u_department,True)
    ivalues = (UserProfile.get_UserProfile(request.user)).group_values(True)
    bars = UserProfile.resume_in_time(userp,datetime.now()-timedelta(days=30),datetime.now())
    usershierarchy = request.user.profile.get_users_hierarchy()
    lastten = Activity.last_ten_of_user(userp)
    usertickets = Ticket.objects.filter(t_usersolver=userp)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link = ''
    link ='TicketsApp/users_id.html'
    return render(request, link, 
            {'userjob':userjob,'dephierarchy':dephierarchy,'servers': servers,'tctype':tctype,'services' : services,'usershierarchy':usershierarchy,'userp':userp,
             'lastten':lastten,'usertickets':usertickets,'notifications':notifications,'bars':bars,'ivalues':ivalues,'bvalues': types,
             })

@login_required(login_url ='')
def users(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    department = Department.objects.get(d_id=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    usershierarchy = department.from_did_get_depusers()
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link ='TicketsApp/users_list.html'
    return render(request, link, 
            {'userjob':userjob,'department':department,'dephierarchy':dephierarchy,'tctype':tctype,'servers': servers,
             'services' : services,'usershierarchy':usershierarchy,'notifications':notifications,
             })

def users_id(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userp= User.objects.get(pk=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    types = []
    for ttype in ttypes:
        types += Ticket.count_types(request.user,dephierarchy,False,ttype)
    cake = []
    for ttype in ttypes:
        cake += [(UserProfile.get_UserProfile(request.user)).group_values(ttype)]
    bars = UserProfile.resume_in_time(userp,datetime.now()-timedelta(days=30),datetime.now())
    usershierarchy = request.user.profile.get_users_hierarchy()
    lastten = Activity.last_ten_of_user(userp)
    usertickets = Ticket.objects.filter(t_usersolver=userp)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link = ''
    link ='TicketsApp/users_id.html'
    return render(request, link, 
            {'userjob':userjob,'dephierarchy':dephierarchy,'tctype':tctype,'servers': servers,'services' : services,'usershierarchy':usershierarchy,'userp':userp,
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

def personal(request,pk):
    thistype = Ttype.objects.filter(id=pk)
    userjob = UserProfile.get_jobtitle(request.user)
    dephierarchy = request.user.profile.from_level_get_dep()
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    psolicitudes = Ticket.tickets(request.user,userdepartment,True,thistype)
    link ='TicketsApp/personal.html'
    return render(request, link, {'userjob':userjob,'userdepartment':userdepartment,
             'dephierarchy':dephierarchy,
             'tctype':tctype,'thistype':thistype,
             'psolicitudes':psolicitudes,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,})

def group(request,pk2,pk1):
    thistype = Ttype.objects.filter(id=pk2)
    thisdepartment = Department.objects.filter(d_id=pk1)
    userjob = UserProfile.get_jobtitle(request.user)
    dephierarchy = request.user.profile.from_level_get_dep()
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    gsolicitudes = Ticket.objects.filter(t_department=thisdepartment,t_ttype=thistype)
    link ='TicketsApp/group.html'
    return render(request, link, {'userjob':userjob,'userdepartment':userdepartment,
             'dephierarchy':dephierarchy,
             'tctype':tctype,'thistype':thistype,'thisdepartment':thisdepartment,'gsolicitudes':gsolicitudes,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,})

def ptasks(request):
    userjob = UserProfile.get_jobtitle(request.user)
    dephierarchy = request.user.profile.from_level_get_dep()
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    ptasks = Ticket.tasks(request.user)
    link ='TicketsApp/tasks.html'
    return render(request, link, {'userjob':userjob,'userdepartment':userdepartment,
             'dephierarchy':dephierarchy,
             'tctype':tctype,'ptasks':ptasks,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,})

def ticket(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    dephierarchy = request.user.profile.from_level_get_dep()
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    taskcount = Ticket.task_count(request.user)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
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
        link ='TicketsApp/ticketid.html'
        return render(request,link,{
             'userjob':userjob,'userdepartment':userdepartment,
             'dephierarchy':dephierarchy,
             'tctype':tctype,'ptasks':ptasks,    
             'servers': servers,'services' : services,'taskcount' : taskcount,
             'notifications':notifications,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
            'services':services,'dateopen':dateopen,})
    else: return render(request,'TicketsApp/page_404.html')

def ticket_create(request,pk):
    ttype = Ttype.objects.get(ty_name=pk)
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
    servers = Server.server_count()
    services = Service.service_count()
    usersofdep = userdepartment.from_did_get_depusers()
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    if request.method =="POST":
        formTicket = CreateTicketForm(request.POST)
        ticketpk = formTicket.save(commit=False)
        ticketpk.t_userreporter = request.user
        ticketpk.t_state = ttype.ty_workflow.w_start
        ticketpk.t_ttype = ttype    
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
        return render(request,'TicketsApp/ticketid_create.html',{
        'userjob':userjob,'dephierarchy':dephierarchy,'tctype':tctype,'ttypes':ttypes,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
        'ttype':ttype,
             })
    
def ticket_edit(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
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
    usersofdep = userdepartment.from_did_get_depusers()
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link ='TicketsApp/'
    if request.method =="POST":
        formTicket = EditTicketStateForm(request.POST, instance = ticketpk)
        formTicket.fields['t_state'].queryset = Action.posible_states(ticketpk.t_state)
        final = State.objects.get(pk=request.POST.get('t_state')) 
        newactivity = Activity.insert(ticketpk,
            final.s_name,
            request.user,datetime.now(),
            "El estado ha sido cambiado de "+ticketpk.t_state.s_name+" a "+str(final.s_name))
        newactivity.save()
        ticketpk = formTicket.save(commit=False)
        ticketpk.usersolver=request.user
        ticketpk.save()
        return render(request, link+'ticketid.html',{
        'userjob':userjob,'dephierarchy':dephierarchy,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,'ttypes':ttypes,'tctype':tctype,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
        'services':services,'notifications':notifications,
         })
    else:
        formTicket = EditTicketStateForm(instance=ticketpk)
        formTicket.fields['t_state'].queryset = Action.posible_states(ticketpk.t_state)
        return render(request,link+'ticketid_edit.html',{
        'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
         })

def ticket_attach(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
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
    usersofdep = userdepartment.from_did_get_depusers()
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link = 'TicketsApp/'  
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
         'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
        'services':services,'archiveattached':archiveattached,'notifications':notifications,
         })
    else:
        formArchive = AddArchiveForm(instance=ticketpk)
        return render(request,link+'ticketid_attach.html',{
         'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,
        'services':services,'usersofdep':usersofdep,'formArchive':formArchive,'notifications':notifications,
         })

def ticket_scale(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
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
    usersofdep = request.user.profile.u_department.from_did_get_depusers()
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link = 'TicketsApp/'
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
        'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
        'services':services,'notifications':notifications,
         })
    else:
        formTicket = EditScaleForm(instance=ticketpk)
        return render(request,link+'ticketid_scale.html',{
        'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
        'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
        'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
        'sons':sons,'activities':activities,'lastactivity':lastactivity,
        'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
        'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
         }) 

def ticket_transfer(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
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
    usersofdep = userdepartment.from_did_get_depusers()
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    link ='TicketsApp/'  
    if request.method =="POST":
        formActivity = TransferForm(request.POST, instance = ticketpk)
        newactivity = Activity.insert(ticketpk,
            "Transferencia",
            request.user,datetime.now(),
            "El ticket ha sido transferido de "+ticketpk.t_usersolver.get_full_name()+" a \'  \' \n a razon de: \n"+str(request.POST.get('at_description')))
        newactivity.save()
        ticketpk.t_usersolver = ticketpk.t_userreporter
        ticketpk.t_department = UserProfile.get_department(ticketpk.t_userreporter)
        ticketpk.save()
        return render(request,'TicketsApp/ticketid.html',{
            'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers,   
            'services':services,'notifications':notifications,
             })
    else:
        formTicket = TransferForm(instance=ticketpk)
        return render(request,'TicketsApp/ticketid_transfer.html',{
            'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
            'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
             })
    
def ticket_assign(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    ttypes = Ctype.objects.filter(ct_company=request.user.profile.u_company)
    tctype = Ticket.ticket_counts(request.user,dephierarchy,ttypes)
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
    usersofdep = userdepartment.from_did_get_depusers()
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    firststateoncompany = request.user.profile.u_company.start_of_workflows_of()
    notifications = Ticket.notifications(request.user,firststateoncompany)
    hierarchy = UserProfile.get_users_hierarchy(request.user.profile)
    link ='TicketsApp/'  
    if request.method =="POST":
        formActivity = AsignateSolverTicketForm(request.POST, instance = ticketpk)
        if ticketpk.t_usersolver == None :
            newactivity = Activity.insert(ticketpk,
                "Asignado",
                request.user,datetime.now(),
                "El ticket ha sido asignado a "+str(User.objects.get(username=request.POST.get('t_usersolver')).get_full_name()) +" \n")
        else:
            newactivity = Activity.insert(ticketpk,
                "Asignado",
                request.user,datetime.now(),
                "El ticket ha sido asignado de "+ticketpk.t_usersolver.get_full_name()+" a "+str(User.objects.get(username=request.POST.get('t_usersolver')).get_full_name()) +" \n")
        newactivity.save()
        ticketpk.t_usersolver = User.objects.get(username=request.POST.get('t_usersolver'))
        ticketpk.t_department = UserProfile.get_department(ticketpk.t_usersolver)
        ticketpk.save()
        return render(request,link+'ticketid.html',{
            'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 'hierarchy': hierarchy,
            'services':services,'notifications':notifications,
                 })
    else:
        formTicket = AsignateSolverTicketForm(instance=ticketpk)
        formTicket.fields['t_usersolver'].queryset = UserProfile.get_users_hierarchy(request.user.profile).values_list('u_user__username',flat=True)
        return render(request,link+'ticketid_assign.html',{
            'userjob':userjob,'dephierarchy':dephierarchy,'ttypes':ttypes,'tctype':tctype,'ticketpk':ticketpk,
            'useraffected':useraffected,'usersolver':usersolver,'sla':sla,
            'slahour':slahour,'slaminute':slaminute,'attacheds':attacheds,    
            'sons':sons,'activities':activities,'lastactivity':lastactivity,
            'datesolved':datesolved,'dateclosed':dateclosed,'servers':servers, 
            'services':services,'usersofdep':usersofdep,'formTicket':formTicket,'notifications':notifications,
                 })

def ticket_print(request,pk):
    return ticket_printed(request,pk)

def ticket_close(request,pk):
    dephierarchy = request.user.profile.from_level_get_dep()
    ticketpk = Ticket.objects.get(pk=pk)
    ticketpk.t_issolved = True
    ticketpk.t_state = "Cerrado"
    link ='TicketsApp/'
    newactivity = Activity.insert(ticketpk,
            "Cerrado",
            request.user,
            datetime.now(),
            "El ticket ha sido Cerrado por "+str(request.user.get_full_name()) +" \n")
    newactivity.save()
    ticketpk.save()
    return redirect(reverse('index'))