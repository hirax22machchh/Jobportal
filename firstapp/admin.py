from django.contrib import admin
from firstapp.models import Jobseeker,Employer,Jobposting,Application,Qualification,Login
# Register your models here.
admin.site.register(Jobseeker)
admin.site.register(Employer)
admin.site.register(Application)
admin.site.register(Jobposting)
admin.site.register(Qualification)
admin.site.register(Login)