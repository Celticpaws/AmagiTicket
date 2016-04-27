from django.db import models
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
import os

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


class Management(models.Model):
	m_id = models.IntegerField(unique=True,primary_key=True)
	m_name = models.CharField(max_length=100)
	m_manager = models.ForeignKey('auth.User',default=0)
	m_company = models.ForeignKey('Company',default=0)

	def __str__(self):
		return self.m_name

	def get_man(str):
		return Management.objects.get(m_name=str)

	def from_user_get_manusers(User):
		manuser = UserProfile.get_management(User)
		man = Management.get_man(manuser)
		users = UserProfile.objects.filter(u_management=man)
		return users

	def leader_of_management(self):
		return self.m_manager


class Department(models.Model):
	d_id = models.IntegerField(unique=True)
	d_name = models.CharField(max_length=100,primary_key=True)
	d_manager = models.ForeignKey('auth.User',default=0)
	d_management = models.ForeignKey('Management',default=0)

	def __str__(self):
		return self.d_name

	def get_did(str):
		return Department.objects.get(d_name=str)

	def from_user_get_depusers(User):
		depuser = UserProfile.get_department(User)
		did = Department.get_did(depuser)
		users = UserProfile.objects.filter(u_department=did)
		return users

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
	u_secondlastname = models.CharField(max_length=30)
	u_phone = models.ForeignKey('Phone')
	u_jobtitle = models.CharField(max_length=100)
	u_department = models.ForeignKey('Department',default=0)
	u_management = models.ForeignKey('Management',default=0)
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
		man = self.u_management
		if (self == did.leader_of_department().profile):
			return  User.objects.filter(profile__u_department=did)
		if (self == man.leader_of_management().profile):
			return User.objects.filter(profile__u_management=man)
		else:
			return User.objects.filter(profile=self)

	def solicitude_group_values(self):
		users = self.get_users_hierarchy()
		none = Ticket.none_count(self,False)
		personal = Ticket.ticket_count(self.u_user,True,False)
		group = Ticket.ticket_count(self.u_user,False,False)
		res=[["No asignados",none]]
		userdep = self.u_department
		if (userdep.leader_of_department() == self.u_user):
			for user in users:
				res += [[user.get_full_name,Ticket.ticket_count(user,True,False)]]
		else: 
			res += [[self.u_user.get_full_name,personal]]
			res += [[userdep,group-none-personal]]
		return res

	def incident_group_values(self):
		users = self.get_users_hierarchy()
		none = Ticket.none_count(self,True)
		personal = Ticket.ticket_count(self.u_user,True,True)
		group = Ticket.ticket_count(self.u_user,False,True)
		res=[["No asignados",none]]
		userdep = self.u_department
		if (userdep.leader_of_department() == self.u_user):
			for user in users:
				res += [[user.get_full_name,Ticket.ticket_count(user,True,True)]]
		else: 
			res += [[self.u_user.get_full_name,personal]]
			res += [[userdep,group-none-personal]]
		return res


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
		


class Ticket(models.Model):
	t_id = models.IntegerField(primary_key=True)
	t_mother = models.ForeignKey('Ticket',related_name='t_mother_of',default=0,null=True,blank=True)
	t_isincident = models.BooleanField(default=False)
	t_useraffected = models.ForeignKey('auth.User',related_name='t_useraffected',default=0)
	t_category = models.CharField(max_length=20)
	t_title = models.CharField(max_length = 100)
	t_description = models.CharField(max_length=1000)
	t_server =models.ForeignKey('Server')
	t_service = models.ForeignKey('Service')
	t_impact = models.IntegerField()
	t_priority = models.IntegerField()
	t_sla = models.ForeignKey('SLA',related_name='sla')
	t_userreporter = models.ForeignKey('auth.User',related_name='t_userreporter',default=0)
	t_reportmadeon = models.DateTimeField(default=datetime.now())
	t_department = models.ForeignKey('Department')
	t_usersolver = models.ForeignKey('auth.User',related_name='t_usersolver',default=0,null=True)
	t_state = models.CharField(max_length=10)
	t_issolved = models.BooleanField(default=False)
	t_viewers = models.CharField(max_length=1000,default="")

	def __str__(self):
		return '# '+str(self.t_id)

	def none_count(User,isincident):
		nonesolicitude = Ticket.objects.filter(t_isincident=isincident,t_usersolver=None,t_department=User.u_department)
		return nonesolicitude.count()

	def ticket_count(User,ispersonal,isincident):
		if ispersonal:
			ticket = Ticket.objects.filter(t_isincident=isincident,t_usersolver=User)
		else:
			depuser = UserProfile.get_department(User)
			did = Department.get_did(depuser)
			ticket = Ticket.objects.filter(t_isincident=isincident,t_department=did)
		return ticket.count()

	def ticket_count_active(User,isincident):
		p = Ticket.objects.filter(t_isincident=isincident,t_state="Resuelto",t_usersolver=User)| Ticket.objects.filter(t_isincident=isincident,t_state="Cerrado",t_usersolver=User)
		count = Ticket.ticket_count(User,True,isincident)
		if count == 0:
			return 0
		else:
			return (p.count()/count*100)

	def tickets(User,ispersonal,isincident):
		if ispersonal:
			t = Ticket.objects.filter(t_isincident=isincident,t_usersolver=User)
		else:
			depuser = UserProfile.get_department(User)
			did = Department.get_did(depuser)
			t = Ticket.objects.filter(t_isincident=isincident,t_department=did)
		return t

	def get_sons(Ticke):
		sons = Ticket.objects.filter(t_mother=Ticke)
		return sons

	def count_types(User):
		if User.profile.u_department.leader_of_department()==User:
			types = Ticket.objects.filter(t_department=User.profile.u_department).values('t_state').annotate(dcount=Count('t_state'))
		else:
			types = Ticket.objects.filter(t_usersolver=User).values('t_state').annotate(dcount=Count('t_state'))
		order = ['Iniciado','Asignado','En Proceso','En Espera','Re-abierto','Resuelto','Cerrado']
		typesordered = sorted(types, key = lambda p: order.index(p['t_state']))
		arrayoftypes=[]
		for t in typesordered:
			arrayoftypes+=[[t['t_state'],t['dcount']]]
		return arrayoftypes

	def tasks(User):
		if User.profile.u_department.leader_of_department()==User:
			tasks = Ticket.objects.filter(t_state="Asignado",t_department=User.profile.u_department)| Ticket.objects.filter(t_state="En Proceso",t_department=User.profile.u_department)| Ticket.objects.filter(t_state="En Espera",t_department=User.profile.u_department)| Ticket.objects.filter(t_state="Reabierto",t_department=User.profile.u_department)
		else:
			tasks = Ticket.objects.filter(t_state="Asignado",t_usersolver=User)| Ticket.objects.filter(t_state="En Proceso",t_usersolver=User)| Ticket.objects.filter(t_state="En Espera",t_usersolver=User)| Ticket.objects.filter(t_state="Re-abierto",t_usersolver=User)
		
		orderedtasks = tasks.order_by('-t_isincident','t_priority','-t_sla')
		return orderedtasks

	def task_count(User):
		t = tasks(User)
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

	def pop(User):
		tickets = Ticket.objects.filter(t_usersolver=User)
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
		    activitylast = activities[0].at_date
		return activitylast

	def date_of_event(Ticket,String):
		activity = Activity.objects.filter(at_ticket=Ticket,at_tipe=String)
		if (activity.count() == 0):
			if (String == 'Resuelto'):
				solved='No ha sido resuelto'
			if (String == 'Cerrado'):
				solved = 'No ha sido cerrado'
		else:
		    solved=activity[0].at_date
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

	@classmethod
	def insert(cls,ticket,tipe,createdby,date,description):
		activity = cls(
			at_ticket=ticket,
			at_tipe=tipe,
			at_createdby=createdby,
			at_date=date,
			at_description=description) 
		return activity


