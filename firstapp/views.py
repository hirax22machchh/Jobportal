from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import render
from firstapp.models import Jobseeker,Employer,Login,Application,Jobposting,Qualification
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from datetime import date
import random
from django.shortcuts import render, get_object_or_404


#--------------------------------------------------------------------------------------------------------------------------------------

def signup(request):
    if request.method == 'POST':
        if 'jobseeker' in request.POST:
            return render(request, 'j_signup.html')
             
        if 'employer' in request.POST:
            return render(request, 'e_signup.html')
        
    return render(request, 'signup.html')
            

#----------------------------------------------------------------------------------------------------------------------------------------


    
def j_signup(request):
    if request.method == "POST":
        js_name = request.POST.get('jobseeker_name')
        js_email = request.POST.get('email')
        mobileno = request.POST.get('phone_number')
        resume = request.FILES.get('resume')
        js_address = request.POST.get('address')
        birthdate = request.POST.get('birth_date')  
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        
        
        if password != c_password:
            error_message = "your password can not match"
            return HttpResponseBadRequest(error_message)      
            
       
        jobseeker = Jobseeker(
            js_name=js_name,
            js_email=js_email,
            username=username,
            mobileno=mobileno,
            resume=resume,
            js_address=js_address,
            birthdate=birthdate,
            password=password
        )
        #checks the username ,email or mobile number are unique
        try:
            jobseeker.save()
            print("successfull")
        except IntegrityError as e:
             error_message2 = "A Jobseeker with the same username, email, or mobile number already exists. Please try using another details"
             return HttpResponseBadRequest(error_message2)
        
      
    return render(request,'j_login.html')
 
 
 #------------------------------------------------------------------------------------------------------------------------------
def e_signup(request):
    print("successfull")    
    if request.method == "POST":
        emp_name = request.POST.get('employer_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        emp_email = request.POST.get('email')
        help_line_no = request.POST.get('help_line_number')
        industry = request.POST.get('industry')
        location = request.POST.get('location')
        avg_salary = request.POST.get('avg_salary')
        
        if password != c_password:
            error_message = "Your password does not match the confirm password. Please re-enter."
            return HttpResponseBadRequest(error_message)
        
        try:
          employer = Employer(
                emp_name=emp_name,
                emp_email=emp_email,
                username=username,
                help_line_no=help_line_no,
                industry=industry,
                location=location,
                avg_salary=avg_salary,
                password=password
            )
          employer.save()
        except IntegrityError as e:
         error_message = "An Employer with the same username, email, or help line number already exists. Please try using different details."
         return HttpResponseBadRequest(error_message)
    
    return render(request,'e_login.html')

 #--------------------------------------------------------------------------------------------------------------------------------
 
def login(request):
    if request.method == 'POST':
        if 'jobseeker' in request.POST:
            return render(request, 'j_login.html')
             
        if 'employer' in request.POST:
            return render(request, 'e_login.html')
    return render(request,'login.html')
 
 #------------------------------------------------------------------------------------------------------------------------------------
 
def e_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
                employer = Employer.objects.get(username=username)
   
        except Employer.DoesNotExist:
 
            error_message = "Invalid username or password."
            return render(request, 'e_login.html', {'error_message': error_message})

        if (password==employer.password):
           if employer is not None:
            # Authentication successful, redirect to a success page
            login_instance = Login.objects.create(username=username, password=password)
            login_instance.save()
            employer = Employer.objects.get(username=username)
            emp_name = employer.emp_name
            request.session['my_key'] = username
            return render(request,'e_homepage.html',{'emp_name': emp_name})
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password."
            return render(request, 'e_login.html', {'error_message': error_message})


#----------------------------------------------------------------------------------------------------------------------------------------- 
def j_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            jobseeker = Jobseeker.objects.get(username=username)
        except Jobseeker.DoesNotExist:
            # Handle the case where the username doesn't exist in the database
            error_message = "Invalid username or password."
            return render(request, 'j_login.html', {'error_message': error_message})

        if (password == jobseeker.password):
            if jobseeker is not None:
                # Authentication successful, redirect to a success page
                login_instance = Login.objects.create(username=username, password=password)
                login_instance.save()
                jobseeker = Jobseeker.objects.get(username=username)
                js_name = jobseeker.js_name
                request.session['my_key'] = username

                # Retrieve all job postings
                all_job_postings = Jobposting.objects.filter(delete_jobpost=False)

                # Get the count of all job postings
                total_job_postings_count = all_job_postings.count()

                # If there are job postings available
                if total_job_postings_count > 0:
                    # If there are fewer than 5 job postings, get all of them
                    if total_job_postings_count <= 5:
                        random_job_postings = all_job_postings
                    else:
                        # Generate five random indices
                        random_indices = random.sample(range(total_job_postings_count), 5)

                        # Fetch five random job postings
                        random_job_postings = [all_job_postings[index] for index in random_indices]

                    job_postings_list = []

                    for job_posting in random_job_postings:
                        job_posting_row = [
                            job_posting.jp_id,
                            job_posting.emp_id,
                            job_posting.designation,
                            job_posting.vacancies,
                            job_posting.salary,
                            job_posting.req_qualification,
                            job_posting.req_experience,
                        ]
                        job_postings_list.append(job_posting_row)

                    # Now random_job_postings contains the available job postings
                else:
                    # Handle the case where there are no job postings in the database
                    print("There are no job postings in the database.")

                

                return render(request, 'j_homepage.html', {'js_name': js_name, 'random_job_postings': random_job_postings})
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password."
            return render(request, 'j_login.html', {'error_message': error_message})

    

 #------------------------------------------------------------------------------------------------------------------------------------------
 
def j_menu(request):
    if request.method == 'POST':
        if 'profile' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_name = jobseeker.js_name
            js_email = jobseeker.js_email
            js_address = jobseeker.js_address
            mobileno = jobseeker.mobileno
            resume = jobseeker.resume
            birthdate = jobseeker.birthdate
            
          
 
            return render(request, 'j_profile.html',{
    'js_name': js_name,
    'js_email': js_email,
    'js_address': js_address,
    'mobileno': mobileno,
    'resume': resume.url,
    'birthdate': birthdate
        })
         
        elif 'homepage' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_name = jobseeker.js_name
            js_id = jobseeker.js_id
            
            all_job_postings = Jobposting.objects.filter(delete_jobpost=False)

                # Get the count of all job postings
            total_job_postings_count = all_job_postings.count()

                # If there are job postings available
            if total_job_postings_count > 0:
                    # If there are fewer than 5 job postings, get all of them
                    if total_job_postings_count <= 5:
                        random_job_postings = all_job_postings
                    else:
                        # Generate five random indices
                        random_indices = random.sample(range(total_job_postings_count), 5)

                        # Fetch five random job postings
                        random_job_postings = [all_job_postings[index] for index in random_indices]

                    job_postings_list = []

                    for job_posting in random_job_postings:
                        job_posting_row = [
                            job_posting.jp_id,
                            job_posting.emp_id,
                            job_posting.designation,
                            job_posting.vacancies,
                            job_posting.salary,
                            job_posting.req_qualification,
                            job_posting.req_experience,
                        ]
                        job_postings_list.append(job_posting_row)

                    # Now random_job_postings contains the available job postings
            else:
                    # Handle the case where there are no job postings in the database
                    print("There are no job postings in the database.")
            
            return render(request, 'j_homepage.html',{'js_name': js_name,'random_job_postings': random_job_postings,})
        
      
        elif 'qualification' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_name = jobseeker.js_name
            js_id = jobseeker.js_id
            qualifications = Qualification.objects.filter(js_id=js_id)
    
    # Create a list to store qualification data
            qualification_data = []

    # Iterate through each qualification and retrieve its data
            for qualification in qualifications:
               qualification_info = {
               'name': qualification.name,
               'institute': qualification.institute,
               'start_time': qualification.start_time,
               'end_time': qualification.end_time,
               'status': qualification.status
                                   }
               print(qualification_info)
               qualification_data.append(qualification_info)
            return render(request, 'j_qualification.html', {'js_name': js_name, 'qualification_data': qualification_data})
 
            
    
        
        elif 'aboutus' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_name = jobseeker.js_name
            return render(request, 'j_aboutus.html',{'js_name': js_name})
        
        elif 'applied_jobs' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_id = jobseeker.js_id  # Assigning value to js_id
    
            js_name = jobseeker.js_name
            appliedjobs = Application.objects.filter(js_id=js_id)
    
    
            appliedjobs_data = []

    
            for appliedjob in appliedjobs:
               appliedjobs_info = {
               'name': appliedjob.jp_id.emp_id.emp_name,
               'designation': appliedjob.jp_id.designation,  
               'date': appliedjob.app_date,
               'curr_status': appliedjob.curr_status,
               'message': appliedjob.message,
                                   }
               appliedjobs_data.append(appliedjobs_info)
            return render(request, 'j_applied_jobs.html', {'js_name': js_name, 'appliedjobs_data': appliedjobs_data})
            
            
            
        
        elif 'help' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_name = jobseeker.js_name
            return render(request, 'j_help.html',{'js_name': js_name})
    
        elif 'logout' in request.POST:
            my_value = request.session.get('my_key')
        
            username = my_value
            last_login_time = get_last_login_time(username)
            if last_login_time:
                   print(f"Last login time for {username}: {last_login_time}")
            else:
                   print(f"No login records found for username '{username}'.")
            
              
            request.session.clear()
            request.session.flush()
            return render(request, 'signup.html')
        
        elif 'add_qualification' in request.POST:
            return render(request, 'j_qualification_form.html')
        
#---------------------------------------------------------------------------------------------------------------------------------------------


def search(request):
    if request.method == 'POST':
        my_value = request.session.get('my_key')
        jobseeker = Jobseeker.objects.get(username=my_value)
        js_name = jobseeker.js_name
        search_criteria = request.POST.get('search_criteria')
        search_query = request.POST.get('search_query')
        print("Search Criteria:", search_criteria)
        print("Search Query:", search_query)

        # Perform the search query based on the selected criteria
        if search_criteria == 'designation':
            results = Jobposting.objects.filter(designation__icontains=search_query, delete_jobpost=False)
        elif search_criteria == 'emp_name':
            results = Jobposting.objects.filter(emp_id__emp_name__icontains=search_query, delete_jobpost=False)
        elif search_criteria == 'salary':
            results = Jobposting.objects.filter(salary__icontains=search_query, delete_jobpost=False)
        else:
            results = []  

        return render(request, 'search_results.html', {'results': results,'js_name':js_name})

#-----------------------------------------------------------------------------------------------------------------------------------------------
def job_details(request, job_id):
    my_value = request.session.get('my_key')
    jobseeker = Jobseeker.objects.get(username=my_value)
    js_name = jobseeker.js_name
    job = Jobposting.objects.get(jp_id=job_id)
    return render(request, 'j_applyforjob.html', {'job': job,'js_name':js_name})




def j_applyforjob(request):
    if request.method == 'POST':
        job_id = request.POST.get('applyforjob')
        my_value = request.session.get('my_key')
        
        
        jobseeker = get_object_or_404(Jobseeker, username=my_value)
        
        if not job_id:
            return HttpResponse("No job ID provided.")
        
        jobposting = get_object_or_404(Jobposting, pk=job_id)
        
        # Check if the user has already applied for this job
        existing_application = Application.objects.filter(js_id=jobseeker, jp_id=jobposting).exists()
        if existing_application:
            return HttpResponse("You have already applied for this job.")
        
        # If the user hasn't applied yet, create a new application
        app = Application.objects.create(
            js_id=jobseeker,
            jp_id=jobposting,
            app_date=date.today(),
            message=None,
        )
        app.save()
        
        return HttpResponse("Application submitted successfully!")
    
    return HttpResponse("Failed to submit application!")


    

#---------------------------------------------------------------------------------------------------------------------------------------------

def j_qualification(request):
    if request.method == 'POST':
        if 'j_qualification_submit' in request.POST:
            my_value = request.session.get('my_key')
            jobseeker = Jobseeker.objects.get(username=my_value)
            js_id = jobseeker.js_id 
            js_name = jobseeker.js_name
            #for fetching post data from j_qualification_form.html
            name = request.POST.get('name')
            institute = request.POST.get('institute')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            status = request.POST.get('status')
            qualification = Qualification(
                js_id=jobseeker,
                name=name,
                institute=institute,
                start_time=start_time,
                end_time=end_time,
                status=status,
                
            )
            qualification.save()
            qualifications = Qualification.objects.filter(js_id=js_id)
    
    # Create a list to store qualification data
            qualification_data = []

    # Iterate through each qualification and retrieve its data
            for qualification in qualifications:
               qualification_info = {
               'name': qualification.name,
               'institute': qualification.institute,
               'start_time': qualification.start_time,
               'end_time': qualification.end_time,
               'status': qualification.status
                                   }
               print(qualification_info)
               qualification_data.append(qualification_info)
            return render(request, 'j_qualification.html', {'js_name': js_name, 'qualification_data': qualification_data})

 #------------------------------------------------------------------------------------------------------------------------------------------
 
 
def e_menu(request):
    if request.method == 'POST':
        if 'profile' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_name = employer.emp_name
            emp_email = employer.emp_email
            help_line_no = employer.help_line_no
            industry = employer.industry
            location = employer.location
            avg_salary = employer.avg_salary
            return render(request, 'e_profile.html',{
    'emp_name': emp_name,
    'emp_email': emp_email,
    'help_line_no': help_line_no,
    'industry': industry,
    'location': location,
    'avg_salary': avg_salary,
        })
         

         
        elif 'homepage' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_name = employer.emp_name
            return render(request, 'e_homepage.html',{'emp_name': emp_name})
          
        elif 'postedjobs' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_name = employer.emp_name
            emp_id = employer.emp_id
            jobposting = Jobposting.objects.filter(emp_id=emp_id,delete_jobpost=0)
    
    # list to store qualification data
            jobposting_data = []

    # Iterate through each qualification and retrieving its data
            for jobpost in jobposting:
               jobpost_info = {
               'jp_id':jobpost.pk,   
               'designation': jobpost.designation,
               'vacancies': jobpost.vacancies,
               'salary':jobpost.salary,
               'req_qualification': jobpost.req_qualification,
               'req_experience': jobpost.req_experience
                                   }
               print(jobpost_info)
               jobposting_data.append(jobpost_info)
            return render(request, 'e_postjob.html', {'emp_name': emp_name, 'jobposting_data': jobposting_data})
 
            
    
    
    
    
        
        elif 'aboutus' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_name = employer.emp_name
            return render(request, 'e_aboutus.html',{'emp_name': emp_name})
        
    
        elif 'help' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_name = employer.emp_name
            return render(request, 'e_help.html',{'emp_name': emp_name})
        
        
    
        elif 'logout' in request.POST:
            my_value = request.session.get('my_key')
        
            username = my_value
            last_login_time = get_last_login_time(username)
            if last_login_time:
                   print(f"Last login time for {username}: {last_login_time}")
            else:
                   print(f"No login records found for username '{username}'.")
            
              
            request.session.clear()
            request.session.flush()
            return render(request, 'signup.html')
        
        
        elif 'add_jobpost' in request.POST:
            return render(request, 'e_postjob_form.html')
#------------------------------------------------------------------------------------------------------------------------------------------
 
 
def e_postjob(request):
    if request.method == 'POST':
        if 'e_postjob_submit' in request.POST:
            my_value = request.session.get('my_key')
            employer = Employer.objects.get(username=my_value)
            emp_id = employer.emp_id 
            emp_name = employer.emp_name
            #for fetching post data from E-postjob_form.html
            designation = request.POST.get('designation')
            vacancies = request.POST.get('vacancies')
            salary = request.POST.get('salary')
            req_qualification = request.POST.get('req_qualification')
            req_experience = request.POST.get('req_experience')
            postjob = Jobposting(
                emp_id=employer,
                designation=designation,
                vacancies=vacancies,
                salary=salary,
                req_qualification=req_qualification,
                req_experience=req_experience,
                
            )
            postjob.save()
            jobposting = Jobposting.objects.filter(emp_id=emp_id,delete_jobpost=0)
    
    # list to store qualification data
            jobposting_data = []
            
    # Iterate through each qualification and retrieving its data
            for jobpost in jobposting:
               jobpost_info = {
               'jp_id' : jobpost.jp_id,    
               'designation': jobpost.designation,
               'vacancies': jobpost.vacancies,
               'salary':jobpost.salary,
               'req_qualification': jobpost.req_qualification,
               'req_experience': jobpost.req_experience
                                   }
               jobposting_data.append(jobpost_info)
            return render(request, 'e_postjob.html', {'emp_name': emp_name, 'jobposting_data': jobposting_data})
 
 #----------------------------------------------------------------------------------------------------------------------------------------
 
def jobseeker_details(request, jp_id):
    my_value = request.session.get('my_key')
    employer = Employer.objects.get(username=my_value) 
    emp_name = employer.emp_name
    # Retrieve the job posting object using the provided jp_id
    print("jp_id:", jp_id)  # Print the received jp_id
    job = get_object_or_404(Jobposting, jp_id=jp_id)
    

            # Retrieve the jobposting object using the provided jp_id
    jobposting = get_object_or_404(Jobposting, jp_id=jp_id)

        # Retrieve all applications for the given jobposting
    applications = Application.objects.filter(jp_id=jobposting)

        # Initialize an empty list to store jobseeker details
    jobseeker_details = []

        # Iterate over each application and extract jobseeker details
    for application in applications:
            jobseeker = application.js_id
            jobseeker_detail = {
                'js_id': jobseeker.js_id,
                'js_name': jobseeker.js_name,
                'js_email': jobseeker.js_email,
                'js_address': jobseeker.js_address,
                'mobileno': jobseeker.mobileno,
                'resume': jobseeker.resume.url,  # Assuming you want to get the URL of the resume
                'birthdate': jobseeker.birthdate,
                'application_id': application.app_id,
                'curr_status': application.curr_status,
                'message': application.message
            }
            
            # Fetch qualifications for the current jobseeker
            qualifications = Qualification.objects.filter(js_id=jobseeker)
            qualifications_list = []
            for qualification in qualifications:
                qualification_info = {
                    'name': qualification.name,
                    'institute': qualification.institute,
                    'start_time': qualification.start_time,
                    'end_time': qualification.end_time,
                    'status': qualification.status
                }
                qualifications_list.append(qualification_info)
            
            jobseeker_detail['qualifications'] = qualifications_list

            jobseeker_details.append(jobseeker_detail)


    
    return render(request, 'e_getdetialsof_jobskeers.html', {'job': job,'jobseeker_details':jobseeker_details,'emp_name':emp_name})

def update_status(request, app_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, app_id=app_id)
        new_status = request.POST.get('curr_status')
        application.curr_status = new_status
        application.save()
        return redirect('jobseeker_details', jp_id=application.jp_id.pk)

def add_message(request, app_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, app_id=app_id)
        new_message = request.POST.get('message')
        application.message = new_message
        application.save()
        return redirect('jobseeker_details', jp_id=application.jp_id.pk) 
 
 
 #-----------------------------------------------------------------------------------------------------------------------------------------
 
def close_job_post(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('close')
        if job_post_id:
            job_post = Jobposting.objects.get(pk=job_post_id)
            job_post.delete_jobpost = True
            job_post.save()
            return redirect(e_getjobpost)
        
def e_getjobpost(request):
    
        my_value = request.session.get('my_key')
        employer = Employer.objects.get(username=my_value) 
        emp_name = employer.emp_name
        emp_id=employer.emp_id
        jobposting = Jobposting.objects.filter(emp_id=emp_id,delete_jobpost=0)
    
    # list to store qualification data
        jobposting_data = []
            
    # Iterate through each qualification and retrieving its data
        for jobpost in jobposting:
               jobpost_info = {
               'jp_id' : jobpost.jp_id,    
               'designation': jobpost.designation,
               'vacancies': jobpost.vacancies,
               'salary':jobpost.salary,
               'req_qualification': jobpost.req_qualification,
               'req_experience': jobpost.req_experience
                                   }
               jobposting_data.append(jobpost_info)
        return render(request, 'e_postjob.html', {'emp_name': emp_name, 'jobposting_data': jobposting_data})
 
#------------------------------------------------------------------------------------------------------------------------------------------
def notlogin(request):
     return render(request,'signup.html')
 
def get_last_login_time(username):
    try:
        last_login_instance = Login.objects.filter(username=username).latest('logintime')
        return last_login_instance.logintime
    except Login.DoesNotExist:
        return None
#-----------------------------------------------------------------------------------------------------------------------------------------------    

