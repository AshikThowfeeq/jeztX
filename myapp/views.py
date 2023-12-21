from django.shortcuts import render
from time import sleep
from django.db.models import Count
from datetime import date, datetime, timedelta
from myapp.split import parse_image_filename_v2,split
from .recognition import final
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import json
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from.models import *
from django.utils.dateparse import parse_datetime
from .models import PersonData, EmployeeCameraAssignment
from .forms import CameraAssignmentForm
from django.utils import timezone

infolder='uploads/From-Local'
ref_folder='uploads/Spider-Man'


def loop(infolder,ref_folder):
     print('Start Recognition')
     count=0
     while True:
          count+=1
          sleep(3)
          final(infolder,ref_folder)
          print(count)


def is_admin_user(user):
    return user.is_superuser


@never_cache
@login_required
@user_passes_test(is_admin_user)
def home(request):
     return render(request, 'home.html')





def login_view(request):
     if request.method == 'POST':
          company_id = request.POST['company_id']
          password = request.POST['password']
          user = authenticate(request, username=company_id, password=password)

          if user is not None:
               if user.is_superuser:
                    login(request, user)
                    return redirect('home')
               else:
                    login(request, user)
                    return redirect('index')
               
          else:
               messages.error(request, 'Invalid company ID or password.')

     return render(request, 'login.html')





def register_view(request):
     if request.method == 'POST':
          company_id = request.POST.get('company_id')
          company_name = request.POST.get('company_name')
          email = request.POST.get('email')
          password = request.POST.get('password')

          # Basic validation
          if not (company_id and company_name and email and password):
               messages.error(request, 'All fields are required.')
               return render(request, 'register.html')

          # Check if user already exists
          if CustomUser.objects.filter(company_id=company_id).exists():
               messages.error(request, 'Company ID already in use.')
               return render(request, 'register.html')

          # Create new user
          user = CustomUser.objects.create(
               company_id=company_id,
               email=email,
               company_name=company_name,  # Assuming 'first_name' stores company name
               password=make_password(password)
          )
          user.save()

          return redirect('login')

     return render(request, 'register.html')
import json, os
from django.http import HttpResponseForbidden
from django.shortcuts import render


@never_cache
@login_required
def viewfromjson(request):
    user_company_id = request.user.company_id
    json_file_path = f'results/{user_company_id}.json'
    company_name = None

    try:
        # Opening and reading the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    # If the file is not found, return an HTTP forbidden response
    except FileNotFoundError:
        return HttpResponseForbidden("JSON file not found for the given company ID.")
    # If the JSON is invalid, treat 'data' as an empty list
    except json.JSONDecodeError:
        data = []

    # Retrieve or create the company object
    company, _ = Company.objects.get_or_create(company_id=user_company_id)

    processed_items = []
    
    for item in data:
        # Extract only the filename from the original path
        original_filename = item['image_path'].split('\\')[-1]

        # Manually assign the folder path and combine it with the extracted filename
        new_image_path = f'uploads/From-Local/{user_company_id}/New/{original_filename}'

        # Rest of your code for processing the data...
        parsed_details = parse_image_filename_v2(original_filename)


        name, employee_id, company_id = split(item['face_recognition'])
        
        # Use the obtained values as needed in your logic
        # ...

        # Create or retrieve the person using the obtained values
        person, _ = Person.objects.get_or_create(
            name=name,
            defaults={'employee_id': employee_id, 'company_id': company_id}
        )


        # Retrieve or create the camera object
        camera_name = parsed_details['camera_name']
        camera, _ = Camera.objects.get_or_create(camera_name=camera_name)

        # Insert or update the data in the database
        person_data, _ = PersonData.objects.update_or_create(
            image_path=new_image_path,
            defaults={
                'age': item['Age'],
                'gender': item['Gender'],
                'pose': item['Pose'],
                'company': company,
                'var1': item['var1'],
                'person': person,
                'camera': camera,  # Assigning the camera object instead of camera_name
                'class_name': parsed_details['class_name'],
                'count': parsed_details['count'],
                'date_created': parsed_details['date_created'],
                'time_created': parsed_details['time_created']
            }
        )

        # Now you can add the person_data to the item dictionary
        item['person_data'] = person_data

        localjsonfile =  f'uploads/From-Local/{user_company_id}/Localjson/server_info.json'

        with open(localjsonfile, 'r') as local_file:
            cameras = json.load(local_file)
            for cam in cameras:
                ServerInfo.objects.update_or_create(
                    id=cam['id'],
                    brand=cam['brand'],
                    cam_name=cam['cam_name'],
                    port=cam['port'],
                    ip_address=cam['ip_address'],
                    username=cam['username'],
                    password=cam['password'],
                    url=cam['url']
                )

        processed_items.append(item)

    # Removing processed items from the original data list
    for item in processed_items:
        data.remove(item)

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file)

         # Retrieve the company name
                
      
    if request.user.is_authenticated:
        company_name = request.user.company_name

   

    

    #Counts
    # todays_attendance_count = Attendance.objects.filter(attendance_date=today).count()
    employee_count = Person.objects.filter(company_id=user_company_id).count()
    company = Company.objects.get_or_create(company_id=user_company_id)
    camera_count = Camera.objects.count()
    


    context = {
        'company_name': company_name,
        'employee_count':employee_count,
        'company_id': user_company_id,
        'camera_count':camera_count,
        
        # Include other context variables as needed
    }

        


    return render(request, 'index.html',context)



def dashboard(request):
    user_company_id = request.user.company_id

    # Get today's date
    today_date = '2023-12-12'
    print(today_date)

    # Retrieve all PersonData objects for the company for the current date
    company_person_data = PersonData.objects.filter(
        company__company_id=user_company_id,
        date_created=today_date
    )

    # Calculate attendance statistics by counting occurrences of each person
    attendance_data = company_person_data.values('person__name').annotate(
        attendance_count=Count('person')
    )

    # Pass attendance_data to the dashboard template
    context = {'attendance_data': attendance_data, 'current_date': today_date, 'company_person_data': company_person_data,}
    return render(request, 'attendance.html', context)



def search_employee(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        # Search for the employee by name (assuming 'query' is the employee name)
        employee = Person.objects.filter(name__icontains=query).first()

        if employee:
            # Retrieve the last seen information for the employee
            last_seen_data = PersonData.objects.filter(person=employee).order_by('-date_created', '-time_created').first()
            context = {'employee': employee, 'last_seen_data': last_seen_data}
            return render(request, 'search_employee.html', context)
        else:
           
            return redirect('search_employee')

    return render(request, 'search_employee.html')

from django.shortcuts import render
from .models import PersonData

def search_persons_by_date(request):
    persons_found = False  # Flag to check if persons are found
    search_performed = False  # Flag to check if a search has been performed

    if request.method == "POST":
        search_performed = True
        search_date = request.POST.get('search_date')
        matched_persons = PersonData.objects.filter(date_created=search_date)
        if matched_persons.exists():
            persons_found = True
        context = {'persons': matched_persons, 'search_date': search_date, 'persons_found': persons_found}
    else:
        context = {'persons': None, 'persons_found': persons_found}

    context['search_performed'] = search_performed
    return render(request, 'date.html', context)


def camera_list(request):
    # Fetch data from the database
    person_data = PersonData.objects.all()
    # Create a dictionary to store camera names, counts, and percentages
    camera_data = {}
    # Calculate the total count
    total_count = sum(data.count for data in person_data)
    for data in person_data:
        camera_id = data.camera_id
        # Calculate the percentage
        percentage = (data.count / total_count) * 100 if total_count else 0
        # If the camera_id is not in the dictionary, add it
        if camera_id not in camera_data:
            camera_data[camera_id] = {
                'name': data.camera.camera_name,
                'count': data.count,
                'percentage': round(percentage, 2),  # Round to 2 decimal places
            }
        else:
            # If the camera_id is already in the dictionary, update the count and percentage
            camera_data[camera_id]['count'] += data.count
            camera_data[camera_id]['percentage'] = (camera_data[camera_id]['count'] / total_count) * 100
    # Pass the data to the template
    context = {'camera_data': camera_data.values(), 'total_count': total_count}
    return render(request, 'camera_list.html', context)


def sorted_person_data(request):
    selected_date = request.GET.get('selected_date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    # Fetch and filter PersonData objects by date_created and time_created
    person_data = PersonData.objects.all()
    if selected_date and start_time and end_time:
        # Concatenate the date and time values
        start_datetime = f"{selected_date} {start_time}"
        end_datetime = f"{selected_date} {end_time}"
        # Filter data based on the datetime range
        person_data = person_data.filter(
            date_created=selected_date,
            time_created__range=[start_time, end_time]
        )
    # Sort data by time_created
    person_data = person_data.order_by('time_created')
    # Render the template with the sorted and filtered data
    return render(request, 'person_data_template.html', {'person_data': person_data})



def search_persons_by_datetime(request):
    persons = None
    search_date = None
    start_time = None
    end_time = None

    if request.method == "POST":
        search_date = request.POST.get('search_date')  # Format: 'YYYY-MM-DD'
        start_time = request.POST.get('start_time')    # Format: 'HH:MM:SS'
        end_time = request.POST.get('end_time')        # Format: 'HH:MM:SS'

        # Assuming time_created is stored in 'HH:MM:SS' format and date_created in 'YYYY-MM-DD'
        if search_date and start_time and end_time:
            persons = PersonData.objects.filter(
                date_created=search_date, 
                time_created__range=[start_time, end_time]
            )

    context = {
        'persons': persons,
        'search_date': search_date,
        'start_time': start_time,
        'end_time': end_time
    }

    return render(request, 'time.html', context)


from django.shortcuts import render
from .models import PersonData

def search_camera_details(request):
    camera_details = None
    employee_custom_id = None
    data_found = False  # Flag to check if data is found

    if request.method == "POST":
        company_id = request.user.company_id
        employee_custom_id = request.POST.get('employee_custom_id')

        if company_id and employee_custom_id:
            camera_details = PersonData.objects.filter(
                company__company_id=company_id, 
                person__employee_id=employee_custom_id
            )
            if camera_details.exists():
                data_found = True  # Set the flag to True if data is found

    context = {
        'camera_details': camera_details,
        'employee_id': employee_custom_id,
        'data_found': data_found  # Pass the flag to the template
    }

    return render(request, 'track.html', context)


def assign_camera_view(request):
    if request.method == 'POST':
        form = CameraAssignmentForm(request.POST)
        if form.is_valid():
            camera = form.cleaned_data['camera']
            employee_id = form.cleaned_data['employee_id']

            # Find the employee by ID
            try:
                person_data = PersonData.objects.filter(person__employee_id=employee_id).first()
                if person_data:
                    person = person_data.person
                    EmployeeCameraAssignment.objects.update_or_create(employee=person, cam=camera)
                    return redirect('assign_camera')
                else:
                    form.add_error('employee_id', 'Employee ID not found')
            except PersonData.DoesNotExist:
                form.add_error('employee_id', 'Employee ID not found')

    else:
        form = CameraAssignmentForm()

    # Fetch all cameras and their assigned employees
    camera_assignments = EmployeeCameraAssignment.objects.select_related('cam', 'employee')
    camera_employee_data = {}
    for assignment in camera_assignments:
        if assignment.cam.cam_name not in camera_employee_data:
            camera_employee_data[assignment.cam.cam_name] = []
        camera_employee_data[assignment.cam.cam_name].append(assignment.employee.employee_id)

    print(camera_employee_data)
    


    return render(request, 'assign_camera.html', {'form': form})

