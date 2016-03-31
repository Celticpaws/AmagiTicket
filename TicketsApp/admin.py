from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Phone)
admin.site.register(Company)
admin.site.register(Management)
admin.site.register(Department)
admin.site.register(Disk)
admin.site.register(Server)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Ticket)