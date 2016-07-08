from django.db import models
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
import os
import time

# Create your models here.

def get_name(User):
	if User == None:
		return ''
	else:
		return User.get_full_name()


class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe estar en formato: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list

    def __str__(self):
    	return str(self.phone_number)


class Company(models.Model):
	c_id = models.IntegerField(unique=True,primary_key=True)
	c_name = models.CharField(max_length=100)
	c_owner = models.ForeignKey('auth.User',default=0)

	def __str__(self):
		return self.c_name

	def start_of_workflows_of(self):
		ct= Ctype.objects.filter(ct_company=self)
		s=[]
		for c in ct:
			s += [c.ct_type.ty_workflow.w_start]
		return s

class Ctype(models.Model):
	ct_company = models.ForeignKey('Company')
	ct_type = models.ForeignKey('Ttype')

	def __str__(self):
		return self.ct_company.c_name+" - "+self.ct_type.ty_name

class Member(models.Model):
	m_user = models.ForeignKey('auth.User')
	m_department = models.ForeignKey('Department')

	def __str__(self):
			return self.m_user.get_full_name()+" - "+self.m_department.d_name

	def by_user(user):
		return Member.objects.get(m_user=user)

	def by_department(department):
		return Member.objects.get(m_department=department)

class Department(models.Model):
	d_id = models.IntegerField(unique=True)
	d_name = models.CharField(max_length=100,primary_key=True)
	d_level = models.IntegerField(default=0)
	d_manager = models.ForeignKey('auth.User',default=0)
	d_haveview = models.ManyToManyField('auth.User', through ='Member',related_name='viewers')
	d_management = models.ForeignKey('Department',related_name='d_superior',default=0,null=True,blank=True)

	def __str__(self):
		return self.d_name

	def get_did(str):
		return Department.objects.get(d_name=str)

	def from_did_get_depusers(self):
		sons = self.from_did_get_sondids()
		users = UserProfile.objects.filter(u_department=self)
		if sons:
			for son in sons:
				users = users | son.from_did_get_depusers()
		return users

	def from_did_get_sondids(self):
		sons = Department.objects.filter(d_management=self)
		return sons

	def leader_of_department(self):
		return self.d_manager

class Disk(models.Model):
	dsk_id = models.IntegerField(primary_key=True)
	dsk_name = models.CharField(max_length=20)
	dsk_capacity = models.IntegerField()
	dsk_usage = models.IntegerField()
	dsk_srv = models.ForeignKey('Server',default=0)

	def __str__(self):
		return self.dsk_id


class Server(models.Model):
	srv_name = models.CharField(max_length=50,primary_key=True)
	srv_ip = models.GenericIPAddressField()
	srv_gateway = models.GenericIPAddressField()
	srv_so = models.CharField(max_length=100)
	srv_memory = models.IntegerField() 

	def __str__(self):
		return self.srv_name

	def server_count():
		servers = Server.objects.all()
		return servers.count()

class Service(models.Model):
	svc_id = models.IntegerField(primary_key=True)
	svc_name = models.CharField(max_length=50)
	svc_server = models.ForeignKey('Server',default=0)
	svc_ison = models.BooleanField() 

	def __str__(self):
		return self.svc_name

	def service_count():
		servers = Service.objects.all()
		return servers.count()


class UserProfile(models.Model):
	u_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True,default=0,related_name="profile")
	u_secondname = models.CharField(max_length=30)
	u_accesslevel = models.IntegerField(default=0)
	u_secondlastname = models.CharField(max_length=30)
	u_phone = models.ForeignKey('Phone')
	u_jobtitle = models.CharField(max_length=100)
	u_department = models.ForeignKey('Department',default=0)
	u_company = models.ForeignKey('Company',default=0)
	u_cancreatetickets = models.BooleanField(default=False)

	def __str__(self):
		return self.u_user.get_full_name()

	def get_UserProfile(User):
		if User == None:
			return None
		else:
			up = UserProfile.objects.get(u_user=User)
			return up

	def get_User(self):
		return self.u_user

	def get_jobtitle(User):
		up = UserProfile.objects.get(u_user=User)
		return up.u_jobtitle

	def get_department(User):
		return (UserProfile.objects.get(u_user=User)).u_department

	def get_users_hierarchy(self):
		did = self.u_department
		if (self == did.leader_of_department().profile):
			sons = did.from_did_get_depusers()
			return  sons
		else:
			return User.objects.filter(profile=self)

	def group_values(self,ttype):
		personal = Ticket.ticket_count(self.u_user,self.u_department,True,ttype)
		res = []
		userdep = self.u_department
		if (userdep.leader_of_department() == self.u_user):
			sons = userdep.from_did_get_sondids()
			if sons :
				res=[["No asignados",0]]
				for son in sons:
					res += [[son.d_name,Ticket.ticket_count(None,son,False,ttype)]]
			else:
				none = Ticket.ticket_count(None,userdep,True,ttype)
				res=[["No asignados",none]]
				users = self.get_users_hierarchy()
				for user in users:
					res += [[user.u_user.get_full_name(),Ticket.ticket_count(user.u_user,user.u_department,True,ttype)]]
		else: 
			none = Ticket.ticket_count(None,userdep,False,ttype)
			res=[["No asignados",none]]
			group = Ticket.ticket_count(self.u_user,self.u_department,False,ttype)
			res += [[self.u_user.get_full_name,personal]]
			res += [[userdep,group-none-personal]]
		return res

	def resume_in_time(User,datestart,datefinish):
		tickets = Ticket.objects.filter(t_usersolver=User,t_reportmadeon__gte=datestart,t_reportmadeon__lte=datefinish)
		values = []
		asienp = 0
		enpres = 0
		rescer = 0
		reares = 0
		for ticket in tickets:
			asienp += Activity.time_between_activities(ticket,"Asignado","En Proceso")
			enpres += Activity.time_between_activities(ticket,"En Proceso","Resuelto")
			rescer += Activity.time_between_activities(ticket,"Resuelto","Cerrado")
			reares += Activity.time_between_activities(ticket,"Re-abierto","Resuelto")
		asienp = asienp /len(tickets)
		enpres = enpres /len(tickets)
		rescer = rescer /len(tickets)
		reares = reares /len(tickets)
		return [[['Tiempo de procesamiento'],[asienp]],
				  [['Tiempo de resolución'],[enpres]],
				  [['Tiempo de cierre'],[rescer]],
				  [['Tiempo de resolución de reaperturas'],[reares]]]

	def from_level_get_dep(self):
		level = self.u_accesslevel
		final = []
		while level > 0:
			dids = Department.objects.filter(d_level=level)
			for did in dids:
				if Member.objects.filter(m_department=did,m_user=self.u_user):
					final += [did]
			level -=1
		return final




class SLA(models.Model):
	s_number = models.IntegerField()
	s_measure = models.CharField(max_length=20)

	def __str__(self):
		return str(self.s_number)+" "+self.s_measure

	def ToDeltaTime(self):
		if (self.s_measure=="dias" or self.s_measure=="dia"):
			return timedelta(days=self.s_number)
		if (self.s_measure=="horas" or self.s_measure=="hora"):
			return timedelta(hours=self.s_number)
		if (self.s_measure=="minutos" or self.s_measure=="minuto"):
			return timedelta(minutes=self.s_number)
		else:
			return timedelta(seconds=self.s_number)
		
class Workflow(models.Model):
	w_name = models.CharField(max_length=100)
	w_start = models.ForeignKey('State',null=True,blank=True)

	def __str__(self):
		return self.w_name

	def states_of (self):
		return State.objects.filter(s_workflow=self)



class State(models.Model):
	s_name = models.CharField(max_length=100)
	s_workflow = models.ForeignKey('Workflow', null=True,blank=True)

	def __str__(self):
		return self.s_workflow.w_name+" - "+self.s_name

class Action(models.Model):
	ac_name = models.CharField (max_length=50)
	ac_state_apply = models.ForeignKey('State',related_name='ac_s_actual')
	ac_next_state = models.ForeignKey('State',related_name='ac_s_next')

	def __str__(self):
		return self.ac_name

class Ttype(models.Model):
	ty_name = models.CharField(max_length=100)
	ty_workflow = models.ForeignKey('Workflow')
	ty_color = models.CharField(max_length=20)
	ty_icon = models.CharField(max_length=40,null=True,blank=True)

	def __str__(self):
		return self.ty_name

class Category(models.Model):
	ca_name = models.CharField(max_length=100)

	def __str__(self):
		return self.ca_name

class Ticket(models.Model):
	t_id = models.IntegerField(primary_key=True)
	t_mother = models.ForeignKey('Ticket',related_name='t_mother_of',default=0,null=True,blank=True)
	t_ttype = models.ForeignKey('Ttype',default=None,null=True,blank=True)
	t_useraffected = models.ForeignKey('auth.User',related_name='t_useraffected',default=0)
	t_category = models.ForeignKey('Category',null=True,blank=True)
	t_title = models.CharField(max_length = 100,null=True)
	t_description = models.CharField(max_length=1000)
	t_server =models.ForeignKey('Server',null=True)
	t_service = models.ForeignKey('Service',null=True)
	t_impact = models.IntegerField()
	t_priority = models.IntegerField()
	t_sla = models.ForeignKey('SLA',related_name='sla')
	t_userreporter = models.ForeignKey('auth.User',related_name='t_userreporter',default=0)
	t_reportmadeon = models.DateTimeField(default=datetime.now())
	t_department = models.ForeignKey('Department')
	t_usersolver = models.ForeignKey('auth.User',related_name='t_usersolver',default=0,null=True,blank=True)
	t_state = models.ForeignKey('State',null=True)
	t_issolved = models.BooleanField(default=False)
	t_viewers = models.CharField(max_length=1000,default="")

	def __str__(self):
		return '# '+str(self.t_id)

	def none_count(User,dep,ttype):
		ticket = []
		sons = dep.from_did_get_sondids()
		if sons :
			for son in sons:
				ticket += Ticket.objects.filter(t_ttype=ttype.ct_type,t_usersolver=None,t_department=son)
		else:
			ticket += Ticket.objects.filter(t_ttype=ttype.ct_type,t_usersolver=None,t_department=dep)
		return len(ticket)

	def ticket_count_deps(User,deps,ispersonal,ttype):
		final =[]
		for ty in ttype:
			final += [[ty.ct_type.ty_name,Ticket.ticket_count_deps(User,deps,ispersonal,ty)]]
		return final

	def ticket_count_dep(User,deps,ispersonal,ttype):
		final =[]
		for dep in deps:
			final += [[dep,Ticket.ticket_count(User,dep,ispersonal,ttype)]]
		return final

	def ticket_counts(User,dep,ttypes):
		final = []
		for ty in ttypes:
			n = ty.ct_type
			p = Ticket.ticket_count(User,User.profile.u_department,True,ty)
			g = Ticket.ticket_count_dep(User,dep,False,ty)
			final += [[n,p,g]]
		return final

	def ticket_count(User,dep,ispersonal,ttype):
		ty = Ttype.objects.get(ty_name=ttype.ct_type)
		t = Ticket.tickets(User,dep,ispersonal,ty)
		count = len(t)
		return count

	def ticket_count_active(User,ttype):
		p = Ticket.objects.filter(t_ttype=ttype,t_state="Resuelto",t_usersolver=User)| Ticket.objects.filter(t_ttype=ttype,t_state="Cerrado",t_usersolver=User)
		count = Ticket.ticket_count(User,User.profile.u_department,True,ttype)
		if count == 0:
			return 0
		else:
			return (p.count()/count*100)

	def tickets_dep(User,deps,ispersonal,ttype):
		final =[]
		if len(deps)>0:
			for dep in deps:
				final += [Ticket.tickets(User,dep,ispersonal,ttype)]
		else: 
			final += [Ticket.tickets(User,deps,ispersonal,ttype)]
		return final

	def tickets(User,dep,ispersonal,ttype):
		if (User == None):
			if ispersonal:
				ticket = Ticket.objects.filter(t_ttype=ttype,t_usersolver=User,t_issolved=False)
			else:
				ticket = Ticket.objects.filter(t_ttype=ttype,t_department=dep,t_issolved=False)
				sons = dep.from_did_get_sondids()
				if sons :
					for son in sons:
						ticket = ticket | Ticket.tickets(User,son,ispersonal,ttype)
				else:
					ticket = ticket | Ticket.objects.filter(t_ttype=ttype,t_department=dep,t_issolved=False)
		else:
			if ispersonal:
				ticket = Ticket.objects.filter(t_ttype=ttype,t_usersolver=User,t_issolved=False)
			else:
				ticket = Ticket.objects.filter(t_ttype=ttype,t_department=dep,t_issolved=False)
				sons = dep.from_did_get_sondids()
				if sons :
					for son in sons:
						ticket = ticket | Ticket.tickets(User,son,ispersonal,ttype)
				else:
					ticket = ticket | Ticket.objects.filter(t_ttype=ttype,t_department=dep,t_issolved=False)
		return ticket

	def get_sons(Ticke):
		sons = Ticket.objects.filter(t_mother=Ticke)
		return sons

	def count_types(User,dep,ispersonal,ttype):
		final = []
		tickets = Ticket.objects.none()
		if ispersonal:
			tickets = Ticket.objects.filter(t_usersolver=User,t_ttype=ttype.ct_type)
		else:
			for d in dep:
				tickets = tickets | Ticket.objects.filter(t_department=d,t_ttype=ttype.ct_type)
		states = ttype.ct_type.ty_workflow.states_of()
		count=[0]*len(states)
		for t in tickets:
			position = [i for i,x in enumerate(states) if x==t.t_state][0]
			count[position]+=1
		arrayoftypes=[]
		i=0
		while i < len(count):
			if count[i]>=0:
				arrayoftypes+=[[states[i].s_name,count[i]]]
			i+=1
		final += [arrayoftypes]
		return final

	def tasks(User):
		state = State.objects.filter(s_name="Cerrado")
		if User.profile.u_department.leader_of_department()==User:
			tasks = Ticket.objects.exclude(t_state=state)
		else:
			tasks = Ticket.objects.exclude(t_state=state)
		
		orderedtasks = tasks.order_by('-t_ttype','t_priority','-t_sla')
		return orderedtasks

	def task_count(User):
		t = Ticket.tasks(User)
		return t.count()


	def delta_life(self):
		lifetime = self.t_sla.ToDeltaTime()
		livingtime = timezone.now()-self.t_reportmadeon
		return livingtime/lifetime*100

	def life_spawn(self):
		s=self.t_reportmadeon+self.t_sla.ToDeltaTime()
		if (s>timezone.now()):
			sla = self.t_reportmadeon-timezone.now()+self.t_sla.ToDeltaTime()
			slahour = sla.seconds//3600
			slaminute = (sla.seconds //60)%60
			if (sla.days <=0):
				strsladays = ""
			else:
				if (sla.days <2):
					strsladays = str(sla.days)+" día "
				else:
					strsladays = str(sla.days)+" días "
			return strsladays+str(slahour)+" horas "+str(slaminute)+" minutos"
		else:
			return "Ticket vencido"

	def notifications(user,firststateoncompany):
		n = Ticket.objects.none()
		for f in firststateoncompany:
			n = n | Ticket.objects.filter(t_department=user.profile.u_department,t_state=f)
		n = n.order_by('-t_reportmadeon')
		return n[:10]

	def pop(User):
		state = State.objects.filter(s_name="Cerrado")		
		tickets = Ticket.objects.filter(t_usersolver=User).exclude(t_state=state)
		ticketsfiltered =[]
		for ticket in tickets.all():
			if (ticket.delta_life() > 50):
				ticketsfiltered += Ticket.objects.filter(t_id=ticket.t_id)
		return ticketsfiltered	

class Archive(models.Model):
	a_id = models.IntegerField(primary_key=True)
	a_ticket = models.ForeignKey('Ticket',on_delete=models.CASCADE,default=0)
	a_name = models.CharField(max_length=100)
	a_route = models.FileField()
	a_description = models.CharField(max_length=1000)
	a_dateattached = models.DateTimeField()
	a_userattacher = models.ForeignKey('auth.User',related_name='a_userattacher',default=0)

	def __str__(self):
		return self.a_name

	def archives_of_a_ticket(Ticket):
		archives = Archive.objects.filter(a_ticket=Ticket)
		return archives
	
	@classmethod
	def insert(cls,ticket,name,route,description,date,userattacher):
		archive = cls(
			a_ticket=ticket,
			a_name = name,
			a_route = route,
			a_description=description,
			a_dateattached=date,
			a_userattacher=userattacher) 
		return archive

class Activity(models.Model):
	at_id = models.IntegerField(primary_key=True)
	at_ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE,default=0)
	at_tipe = models.CharField(max_length=100)
	at_createdby = models.ForeignKey('auth.User',related_name='at_createdby',default=0)
	at_date = models.DateTimeField()
	at_timeinverted = models.DateTimeField(default=datetime.now())
	at_description = models.CharField(max_length=500)
	at_viewers = models.CharField(max_length=1000,default="")


	def activities_of_a_ticket(Ticket):
		activities = Activity.objects.filter(at_ticket=Ticket).order_by('-at_date')
		return activities

	def last_modified(Ticket):
		activities = Activity.objects.filter(at_ticket=Ticket).order_by('-at_date')
		if (activities.count() == 0):
			activitylast='No hay una ultima modificación'
		else:
		    activitylast = activities[0].at_date.strftime("%d de %b del %Y a las %I:%M:%S %p")
		return activitylast

	def date_of_event(Ticket,String):
		if String == "":
			date=Ticket.t_reportmadeon
			solved=date.strftime("%d de %b del %Y a las %I:%M:%S %p")
		else:
			activity = Activity.objects.filter(at_ticket=Ticket,at_tipe=String)
			if (activity.count() == 0):
				if (String == "Resuelto"):
					solved='No ha sido resuelto'
				if (String == "Cerrado"):
					solved = 'No ha sido cerrado'
			else:
				date=activity[0].at_date
				solved=date.strftime("%d de %b del %Y a las %I:%M:%S %p")
		return solved

	def last_ten_of_user(User):
		activities = Activity.objects.filter(at_createdby=User).order_by('-at_date')[:5]
		return activities

	def pop(User):
		tickets = Ticket.objects.filter(t_usersolver=User)
		activities =[]
		for ticket in tickets:
			activities += Activity.activities_of_a_ticket(ticket)
		return activities

	def time_between_activities(ticket,istate,fstate):
		idate = Activity.objects.filter(at_ticket=ticket,at_tipe=istate)
		fdate = Activity.objects.filter(at_ticket=ticket,at_tipe=fstate)
		if len(idate) == 0:
			return -1
		if len(fdate) == 0:
			return -2
		idate=idate[0]
		fdate=fdate[0]
		return (fdate.at_date-idate.at_date).total_seconds()

	@classmethod
	def insert(cls,ticket,tipe,createdby,date,description):
		activity = cls(
			at_ticket=ticket,
			at_tipe=tipe,
			at_createdby=createdby,
			at_date=date,
			at_description=description) 
		return activity


