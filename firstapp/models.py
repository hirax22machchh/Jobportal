from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Jobseeker(models.Model):
    js_id = models.AutoField(primary_key=True)
    js_name = models.CharField(max_length=50,null=False)
    username = models.CharField(max_length=20, unique=True,null=False)
    password = models.CharField(max_length=20,null=False)
    js_email = models.EmailField(max_length=30, unique=True,null=False)
    js_address = models.CharField(max_length=200 , default="your address",null=False)
    mobileno = models.CharField(max_length=10, unique=True,null=False)
    resume = models.FileField(upload_to='Resume/',null=False) 
    birthdate = models.DateField(null=True)
    
    def __str__(self):
        return self.js_name
     
class Employer(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=50,null=False)
    username = models.CharField(max_length=20,unique=True,null=False)
    password = models.CharField(max_length=20,null=False)
    emp_email = models.EmailField(max_length=30,unique=True,null=False)
    help_line_no = models.IntegerField(unique=True,null=False)
    industry = models.CharField(max_length=30,null=False)
    location = models.CharField(max_length=100,null=False)
    avg_salary = models.IntegerField(null=False)
    
    def __str__(self):
        return self.emp_name
    
   
class Jobposting(models.Model):
    jp_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employer, on_delete=models.CASCADE, to_field='emp_id')
    designation = models.CharField(max_length=50,null=False)
    vacancies = models.IntegerField(null=False)
    salary = models.IntegerField(null=False)
    req_qualification = models.CharField(max_length=120,null=False)
    req_experience = models.CharField(max_length=40,null=False)
    delete_jobpost = models.BooleanField(default=0)
    def __str__(self):
        return f"{self.emp_id.emp_name} - {self.designation}"

    
    
class Application(models.Model):
    app_id = models.AutoField(primary_key=True)
    js_id = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, to_field='js_id')
    jp_id = models.ForeignKey(Jobposting, on_delete=models.CASCADE, to_field='jp_id')
    app_date = models.DateField()
    curr_status = models.CharField(max_length=40, default="pending")
    message = models.CharField(max_length=200,null=True)

    def __str__(self):
          return f"{self.jp_id.emp_id.emp_name} - {self.jp_id.designation}- {self.js_id.js_name}"

    
class Qualification(models.Model):
    qual_id = models.AutoField(primary_key=True)
    js_id = models.ForeignKey(Jobseeker,on_delete=models.CASCADE,to_field='js_id')
    name = models.CharField(max_length=40,null=False)
    institute = models.CharField(max_length=20,null=False)
    start_time = models.DateField(null=False)
    end_time = models.DateField(null=False)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES,default='Active')
    
    def __str__(self):
        return self.name
 
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,null=False)
    password = models.CharField(max_length=20,null=False)
    logintime = models.DateTimeField(default=timezone.now,null=False)
    
    def __str__(self):
        return self.username  