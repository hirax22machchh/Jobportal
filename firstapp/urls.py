from django.contrib import admin
from django.urls import path
from firstapp import views

admin.site.site_header = "JOB PORTAL"

urlpatterns = [
    path('', views.signup , name='signup'),
    path('login', views.login , name='login'),
    path('e_login', views.e_login , name='e_login'),
    path('j_login', views.j_login , name='j_login'),
    path('j_signup', views.j_signup , name='j_signup'),
    path('e_signup', views.e_signup , name='e_signup'),
    path('signup', views.notlogin , name='notlogin'),
    path('j_menu', views.j_menu , name='j_menu'),
    path('e_menu', views.e_menu , name='e_menu'),
    path('e_postjob', views.e_postjob , name='e_postjob'),
    path('j_qualification', views.j_qualification , name='j_qualification'),
    path('job/<int:job_id>/', views.job_details, name='job_details'),
    path('update_status/<int:app_id>/', views.update_status, name='update_status'),
    path('jobseeker_details/<int:jp_id>/', views.jobseeker_details, name='jobseeker_details'),
    path('add_message/<int:app_id>/', views.add_message, name='add_message'),
    path('j_applyforjob', views.j_applyforjob , name='j_applyforjob'),
    path('search', views.search, name='search'),
    path('close_job_post', views.close_job_post, name='close_job_post'),
    path('e_getjobpost', views.e_getjobpost, name='e_getjobpost'),


]

