from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

# Create your models here.

class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe estar en formato: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list


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


class Department(models.Model):
	d_id = models.IntegerField(unique=True)
	d_name = models.CharField(max_length=100,primary_key=True)
	d_manager = models.ForeignKey('auth.User',default=0)
	d_management = models.ForeignKey('Management',default=0)

	def __str__(self):
		return self.d_name

	def get_did(str):
		return Department.objects.get(d_name=str)

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

class Service(models.Model):
	svc_id = models.IntegerField(primary_key=True)
	svc_name = models.CharField(max_length=50)
	svc_server = models.ForeignKey('Server',default=0)
	svc_ison = models.BooleanField() 

	def __str__(self):
		return self.svc_name


class UserProfile(models.Model):
	u_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True,default=0)
	u_secondname = models.CharField(max_length=30)
	u_secondlastname = models.CharField(max_length=30)
	u_phone = models.ForeignKey('Phone')
	u_jobtitle = models.CharField(max_length=100)
	u_department = models.ForeignKey('Department',default=0)
	u_management = models.ForeignKey('Management',default=0)
	u_company = models.ForeignKey('Company',default=0)

	def __str__(self):
		return self.u_secondname

	def get_UserProfile(User):
		up = UserProfile.objects.get(u_user=User)
		return up

	def get_jobtitle(User):
		up = UserProfile.objects.get(u_user=User)
		return up.u_jobtitle

	def get_department(User):
		return (UserProfile.objects.get(u_user=User)).u_department



class Ticket(models.Model):
	t_id = models.IntegerField(primary_key=True)
	t_isincident = models.BooleanField()
	t_useraffected = models.ForeignKey('auth.User',related_name='t_useraffected',default=0)
	t_category = models.CharField(max_length=20)
	t_description = models.CharField(max_length=200)
	t_server =models.ForeignKey('Server')
	t_service = models.ForeignKey('Service')
	t_impact = models.IntegerField()
	t_priority = models.IntegerField()
	t_sla = models.DateTimeField()
	t_userreporter = models.ForeignKey('auth.User',related_name='t_userreporter',default=0)
	t_reportmadeon = models.DateTimeField()
	t_department = models.ForeignKey('Department')
	t_usersolver = models.ForeignKey('auth.User',related_name='t_usersolver',default=0)
	t_state = models.CharField(max_length=10)
	t_issolved = models.BooleanField()

	def __str__(self):
		return self.t_description

	def personal_solicitude_count(User):
		psolicitude = Ticket.objects.filter(t_isincident=False,t_usersolver=User)
		return psolicitude.count()

	def personal_incident_count(User):
		pincidents = Ticket.objects.filter(t_isincident=True,t_usersolver=User)
		return pincidents.count()

	def group_solicitude_count(User):
		depuser = UserProfile.get_department(User)
		did = Department.get_did(depuser)
		gsolicitude = Ticket.objects.filter(t_isincident=False,t_department=did)
		return gsolicitude.count()

	def group_incident_count(User):
		depuser = UserProfile.get_department(User)
		did = Department.get_did(depuser)
		gincidents = Ticket.objects.filter(t_isincident=True,t_department=did)
		return gincidents.count()

	def personal_solicitudes(User):
		psolicitudes = Ticket.objects.filter(t_isincident=False,t_usersolver=User)
		return psolicitudes

	def group_solicitudes(User):
		depuser = UserProfile.get_department(User)
		did = Department.get_did(depuser)
		gsolicitudes = Ticket.objects.filter(t_isincident=False,t_department=did)
		return gsolicitudes

	def personal_incidents(User):
		psolicitudes = Ticket.objects.filter(t_isincident=True,t_usersolver=User)
		return psolicitudes

	def group_incidents(User):
		depuser = UserProfile.get_department(User)
		did = Department.get_did(depuser)
		gsolicitudes = Ticket.objects.filter(t_isincident=True,t_department=did)
		return gsolicitudes