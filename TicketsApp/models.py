from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
	u_user = models.ForeignKey('auth.User', unique=True)
	u_secondname = models.CharField(max_length=30)
	u_secondlastname = models.CharField(max_length=30)
	u_jobtitle = models.CharField(max_length=100)
	u_department = models.CharField(max_length=100)
	u_office = models.CharField(max_length=100)
	u_createddate = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.u_secondname

