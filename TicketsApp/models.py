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
	c_id = models.IntegerField(unique=True)
	c_name = models.CharField(max_length=100)
	c_owner = models.ForeignKey('auth.User')


	def __str__(self):
		return self.c_name


class Management(models.Model):
	m_id = models.IntegerField(unique=True)
	m_name = models.CharField(max_length=100)
	m_manager = models.ForeignKey('auth.User')

	def __str__(self):
		return self.m_name


class Department(models.Model):
	d_id = models.IntegerField(unique=True)
	d_name = models.CharField(max_length=100)
	d_manager = models.ForeignKey('auth.User')

	def __str__(self):
		return self.d_name


class UserProfile(models.Model):
	u_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
	u_secondname = models.CharField(max_length=30)
	u_secondlastname = models.CharField(max_length=30)
	u_id = models.IntegerField()
	u_phone = models.ForeignKey('Phone')
	u_jobtitle = models.CharField(max_length=100)
	u_department = models.ForeignKey('Department')
	u_management = models.ForeignKey('Management')
	u_company = models.ForeignKey('Company')
	#u_image = models.ImageField ---------AQUI ME QUEDE

	def __str__(self):
		return self.u_secondname


