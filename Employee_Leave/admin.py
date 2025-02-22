from django.contrib import admin
from .models import *
# Register your models here.
class EmployeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position']

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'status']

admin.site.register(Employee, EmployeAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)