from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    LEAVE_TYPE = [
        ('sick_leave', 'Sick Leave'),
        ('casual_leave', 'Casual Leave'),
        ('paid_leave', 'Paid Leave'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.employee.name} - {self.leave_type}'
