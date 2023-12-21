from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Camera)
admin.site.register(PersonData)
admin.site.register(ServerInfo)
admin.site.register(EmployeeCameraAssignment)