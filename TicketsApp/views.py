from django.shortcuts import render
from django.utils import timezone
from .models import *

# Create your views here.
def auth(request):
	users = UserProfile.objects.filter(u_createddate__lte=timezone.now()).order_by('u_createddate')
	return render(request, 'TicketsApp/auth.html', {'users': users})