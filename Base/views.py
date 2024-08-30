# from django.utils.translation import ugettext_lazy as _ #type:ignore
from django.shortcuts import render, redirect, get_object_or_404 #type:ignore
from django.shortcuts import render, redirect #type:ignore
from django.http import HttpResponse #type:ignore
from django.contrib.auth.decorators import login_required #type:ignore
from .models import *
from django.contrib import messages #type:ignore
from django.contrib.auth import login,logout #type:ignore
from django.contrib.auth.models import User #type:ignore
from django.contrib.auth import authenticate,login as newlogin, logout 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as newlogin
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import FileResponse
from django.urls import reverse
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
import io

from .app import estimate

from PyPDF2 import PdfFileReader
from django.contrib.auth import authenticate, login
import openpyxl
import pdfplumber
# for search report page
from django.db.models import Q
from datetime import datetime

#location validation
from django.http import JsonResponse

# location deletion
from django.db import transaction

# Create your views here.


# def login(request):
#     error_message = None
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Check if both username and password are provided
#         if username and password:
#             # Authenticate user
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 # User is authenticated, log in and redirect
#                 newlogin(request, user)
#                 # Store username and password in session
#                 request.session['username'] = username
#                 request.session['password'] = password
#                 return redirect('Dashboard')
#             else:
#                 # Authentication failed, set error message
#                 error_message = 'Invalid username or password.'
#         else:
#             # Username or password is missing, set error message
#             error_message = 'Username and password are required.'
#     return render(request, 'loginnew.html', {'error_message': error_message})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as newlogin
from django.contrib.auth.models import User
from .models import Employee1

# def login(request):
#     error_message = None
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if username and password:
#             # First, try to authenticate as admin (superuser)
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 # User is admin, log in and redirect
#                 newlogin(request, user)
#                 return redirect('Dashboard')
            
#             # If not authenticated as admin, check against employee credentials
#             try:
#                 employee = Employee1.objects.get(uname=username, passwrd=password)
#                 # Assuming successful authentication, log in and redirect
#                 request.session['username'] = username
#                 request.session['password'] = password
#                 return redirect('Dashboard')  # Adjust the URL name for employee dashboard
#             except Employee1.DoesNotExist:
#                 # Authentication failed for both admin and employee
#                 error_message = 'Invalid username or password.'
#         else:
#             error_message = 'Username and password are required.'

#     return render(request, 'loginnew.html', {'error_message': error_message})

def login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if both username and password are provided
        if username and password:
            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # User is authenticated, log in and redirect
                newlogin(request, user)
                # Store username and password in session
                request.session['username'] = username
                request.session['password'] = password
                return redirect('Dashboard')
            else:
                # Authentication failed, set error message
                error_message = 'Invalid username or password.'
        else:
            # Username or password is missing, set error message
            error_message = 'Username and password are required.'

    return render(request, 'loginnew.html', {'error_message': error_message})


def logout(request):
    authlogout(request)
    return redirect('login')

@login_required
def Dash(request):
    project_count=Project.objects.all().count()
    pending_count=Project.objects.filter(status='pending').count()
    ongoing_count=Project.objects.filter(status='on-progress').count()
    completed_count=Project.objects.filter(status='completed').count()
    context={'data4':project_count,'data1':pending_count,'data2':ongoing_count,'data3':completed_count,}
    return render(request,'landingpage.html',context)


@login_required
def fp(request):
    return render(request,'forgotpassword.html')


@login_required
def data(request):
    return render(request, 'formlist.html')


#location Adding
@login_required
def loc(request):
    
    if request.POST:
        t1=request.POST['t1']
        t2=request.POST['t2']
        t3=request.POST['t3']
        data=Location()
        data.locationname=t2
        data.country=t1
        data.save()
        data1=Location.objects.get(country=t1,locationname=t2)
        data2=LocationTax()
        data2.locationid_id=data1.id
        data2.taxpercentage=t3
        data2.save()
        data4 = Location.objects.all()
        paginator=Paginator(data4,4)
        page_number=request.GET.get('page')
        data4=paginator.get_page(page_number)
        context={'data4':data4 } 
        return render(request,'addloc.html',context)
    else:
        data4 = Location.objects.all()
        paginator=Paginator(data4,4)
        page_number=request.GET.get('page')
        data4=paginator.get_page(page_number)
        context={'data4':data4 }         
        return render(request, 'addloc.html',context)
    
#location edit function   
@login_required
def editloc(request,id):
    
    if request.POST:
        t1=request.POST['t1']
        t2=request.POST['t2']
        t3=request.POST['t3']
        data=Location.objects.get(id=id)
        data.country=t1
        data.locationname=t2
        data.save()
        data1=LocationTax.objects.get(locationid_id=id)
        data1.taxpercentage=t3
        data1.save()
        return redirect('location')
        
    else: 
        products_with_colors = Location.objects.get(id=id)
        context={
            'data':products_with_colors
            }
        return render(request,'editloc.html',context)
#location delete function   
def is_admin(user):
    return user.is_superuser
@login_required
@user_passes_test(is_admin)
def delet(request,id):
    # location = get_object_or_404(Location, id=location_id)
    # location.delete()
    data=LocationTax.objects.get(locationid_id=id)
    data.delete()
    data1=Location.objects.get(id=id)
    data1.delete()
    return redirect('location')  # Redirect to the location list view


#validation Location
@login_required
def check_person_name(request):
    if request.method == 'GET':
        person_name = request.GET.get('product_name', None)
        if person_name:
            # Check if person name exists in the database
            exists = Location.objects.filter(locationname=person_name).exists()
            return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'})

@login_required
def mulprodlist(request):
    if request.method == 'POST':
        product_pdf = request.FILES.get('product_pdf')

        if product_pdf.name.endswith('.pdf'):
            # Read PDF file and extract data
            pdf_reader = PdfFileReader(product_pdf)
            num_pages = pdf_reader.numPages
            products = []

            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                text = page.extract_text()
                # Parse text to extract product data (e.g., name, price, description)
                # Add extracted product data to the 'products' list

            # Save extracted products to the database
            for product_data in products:
                product = Product(**product_data)
                product.save()

            messages.success(request, 'Bulk products added successfully.')
            return redirect('productlist')  # Redirect to the product list page

        else:
            messages.error(request, 'Please upload a valid PDF file.')

    return render(request, 'multiproduct.html')


@login_required
def prodlist(request):
    products = Product.objects.all()
    serial_number = 1
    for product in products:
        product.serial_number = serial_number
        serial_number += 1

    # Split 'projects' into pages with 2 items per page
    paginator = Paginator(products, 2)
    
    page_number = request.GET.get('page')
    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        products_page = paginator.page(paginator.num_pages)
    return render(request, 'productlist.html', {'products': products_page})



@login_required
def addprod(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        product_name = request.POST.get('product_name')
        brand_name = request.POST.get('brand_name')
        price_per_unit = request.POST.get('price_per_unit')
        description = request.POST.get('description')
        item_name = request.POST.get('item_name')
        current_rating = request.POST.get('current_rating')
        fault_current = request.POST.get('fault_current')
        power_factor = request.POST.get('power_factor')
        phase = request.POST.get('phase')
        poles = request.POST.get('poles')
        length = request.POST.get('length')
        height = request.POST.get('height')
        width = request.POST.get('width')
        weight = request.POST.get('weight')

        # Check if all required fields are filled        
        if not (product_code and product_name and brand_name and price_per_unit and description and item_name and current_rating and fault_current and power_factor and phase and  poles and length and height and width and weight):
            messages.error(request, 'All fields are required.')
        
            return redirect('addprod') 
        
        if Product.objects.filter(product_code=product_code).exists():
            messages.error(request, 'Product code already exists. Please choose a different code.')
            return redirect('addprod')


        # Create the Product object and save it to the database
        product = Product.objects.create(
            product_code=product_code,
            product_name=product_name,
            brand_name=brand_name,
            price_per_unit=price_per_unit,
            description=description,
            item_name=item_name,
            current_rating=current_rating,
            fault_current=fault_current,
            power_factor=power_factor,
            phase=phase,
            poles=poles,
            length=length,
            height=height,
            width=width,
            weight=weight
        )
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('prodlist')

    return render(request, 'addproduct.html')


# @login_required
# def changepassword(request):
#     # Retrieve username and password from session
#     sessusername = request.session.get('username')
#     sesspassword = request.session.get('password')
#     context={'pswd':sesspassword}
#     if request.method == 'POST':
        
#         new_password = request.POST.get('nwpswd')
#         confirm_password = request.POST.get('confirmpswd')
        
#         # Check if new password and confirm password match
#         if new_password != confirm_password:
#             messages.error(request, 'New password and confirm password do not match!')
#             return redirect(reverse('changepswd')) # Redirect to the same page to display the error message
       
#         # Authenticate user
#         user = authenticate(username=sessusername, password=sesspassword)
        
#         if user is not None:
#             # Change password for the authenticated user
#             user.set_password(new_password)
#             user.save()
            
#             # Login user to update the session with new password
#             newlogin(request, user)
            
#             messages.success(request, 'Your password was successfully updated!')
#             return render(request,'changepassword.html')  # Redirect to the same page after successful password change
#         # else:
#         #     messages.error(request, 'Current password is incorrect!')
#         #     return redirect(reverse('changepswd'))  # Redirect to the same page to display the error message
    
#     return render(request, 'changepassword.html',context)

# @login_required
# def changepassword(request):
#     # Retrieve username and password from session
#     sessusername = request.session.get('username')
#     print(sessusername)
#     sesspassword = request.session.get('password')
#     print(sesspassword)
#     context={'pswd':sesspassword}
#     if request.method == 'POST':
        
#         new_password = request.POST.get('new_password')
#         print(new_password)
#         confirm_password = request.POST.get('confirm_new_password')
#         print(confirm_password)
        
#         # Check if new password and confirm password match
#         if new_password != confirm_password:
#             messages.error(request, 'New password and confirm password do not match!')
#             return redirect(reverse('changepswd')) # Redirect to the same page to display the error message
       
#         # Authenticate user
#         user = authenticate(username=sessusername, password=sesspassword)
        
#         if user is not None:
#             # Change password for the authenticated user
#             user.set_password(new_password)
#             user.save()
            
#             # Login user to update the session with new password
#             newlogin(request, user)
            
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect(reverse('changepswd'))  # Redirect to the same page after successful password change
#         else:
#             messages.error(request, 'Current password is incorrect!')
#             return redirect(reverse('changepswd'))  # Redirect to the same page to display the error message
    
#     return render(request, 'changepassword.html',context)

from django.contrib.auth import logout

@login_required
def changepassword(request):
    # Retrieve username from session
    sessusername = request.session.get('username')
    
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_new_password')
        print(confirm_password)
        
        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match!')
            return redirect(reverse('changepswd'))  # Redirect to the same page to display the error message
        
        # Authenticate user
        user = authenticate(username=sessusername, password=request.session.get('password'))
        
        if user is not None:
            # Change password for the authenticated user
            user.set_password(new_password)
            user.save()
            
            # Expire current session
            logout(request)
            
            messages.success(request, 'Your password was successfully updated! Please login again.')
            return redirect(reverse('login'))  # Redirect to the login page after successful password change
        else:
            messages.error(request, 'Current password is incorrect!')
            return redirect(reverse('changepswd'))  # Redirect to the same page to display the error message
    
    return render(request, 'changepassword.html')

def reg(request):
    return render(request, 'register.html')

@login_required
def stafflist(request):
    if request.method == 'POST':
        empcode = request.POST['staffcode']
        uname = request.POST['uname']

        # Check if the employee code already exists
        if Employee1.objects.filter(empcode=empcode).exists():
            messages.error(request, 'Entered employee code already exists. Please enter a new one.')
            return render_staff_list(request)

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Entered username already exists. Please enter a new one.')
            return render_staff_list(request)
        
        user = User.objects.create_user(request.POST['uname'],request.POST['mail'],request.POST['password'])
        # user = User.objects.create_user(username, request.POST['mail'], request.POST['password'])
        # user.first_name = request.POST['staffname']
        user.is_staff= True
        user.save()
        # Create user and employee records
        employee = Employee1( 
            userid_id=user.id,  # Assign the id of the created user
            empcode=empcode,
            designation=request.POST['desig'],
            name=request.POST['staffname'],
            address=request.POST['addr'],
            contact=request.POST['contact'],
            email=request.POST['mail'],
            uname = uname,
            passwrd=request.POST['password'],

        )
        employee.save()
        messages.success(request, 'Data added successfully.')

    return render_staff_list(request)

def render_staff_list(request):
    emp = Employee1.objects.order_by('id')  # Assuming 'id' is the field you want to order by
    serial_number = 1
    for i in emp:
        i.serial_number = serial_number
        serial_number += 1

    # Split 'projects' into pages with 2 items per page
    paginator = Paginator(emp, 2)
    
    page_number = request.GET.get('page')
    try:
        emp_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        emp_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        emp_page = paginator.page(paginator.num_pages)
     
    context={'data_zipped':emp_page}
    return render(request, 'stafflist.html', context)


@login_required

def delstaff(request,id):
    ob=Employee1.objects.get(id=id)
    ob.delete()
    user = ob.userid
    ob1=User.objects.get(id=user.id)
    ob1.delete()
    messages.success(request, 'Data deleted successfully.')
    return redirect('stafflist')


@login_required
def editstaff(request,id):
    
    employee = get_object_or_404(Employee1, id=id)
    user = employee.userid
    # print(id)
    # print(user.id)

    if request.method == 'POST':
        empcode = request.POST['staffcode']
        uname = request.POST['uname']

        if User.objects.filter(username=uname).exclude(id=user.id).exists():
            
            messages.error(request, 'Entered username already exists. Please enter a new one.')
            context = {
                 'employee': employee
                }
            return render(request, 'editstaff.html', context)
        sessusername = request.session.get('username')
        print(sessusername)
        print(user.username)
        if user.username==sessusername:
            user.username =  uname
            user.email = request.POST['mail']
            if request.POST['password']:
                user.set_password(request.POST['password'])
                user.save()
        # Update user and employee records
            employee.empcode = empcode
            employee.designation = request.POST['desig']
            employee.address = request.POST['addr']
            employee.contact = request.POST['contact']
            employee.uname = uname
            employee.email = request.POST['mail']
            employee.name = request.POST['staffname']
            employee.passwrd = request.POST['password']
        
            employee.save()
            logout(request)
            
            messages.success(request, 'Your credentials was successfully updated! Please login again.')
            return redirect(reverse('login'))
        
        user.username =  uname
        user.email = request.POST['mail']
        if request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        # Update user and employee records
        employee.empcode = empcode
        employee.designation = request.POST['desig']
        employee.address = request.POST['addr']
        employee.contact = request.POST['contact']
        employee.uname = uname
        employee.email = request.POST['mail']
        employee.name = request.POST['staffname']
        employee.passwrd = request.POST['password']
        employee.save()
        messages.success(request, 'Data updated successfully.')
        return redirect('stafflist')
    context = {
        'employee': employee
        }
    return render(request, 'editstaff.html', context)

   # return render_edit_staff(request, employee)

# def render_edit_staff(request, employee):

#     context = {
#         'employee': employee
#     }
#     return render(request, 'editstaff.html', context)








# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def delstaff(request, emp_id):
#     employee = get_object_or_404(Employee, id=emp_id)
#     user = employee.userid  # Assuming `userid` is a ForeignKey to the `User` model

#     if request.method == 'POST':
#         # First delete the Employee object
#         employee.delete()
#         # Then delete the User object
#         user.delete()
#         messages.success(request, 'Employee deleted successfully.')
#         return redirect('stafflist')

#     context = {
#         'employee': employee,
#         'user': user,
#     }
#     return render(request, 'stafflist.html', context)


@login_required
def addp(request):
    if request.method == 'POST':
        project_code = request.POST.get('project_code')
        project_name = request.POST.get('project_name')
        consultant = request.POST.get('consultant')
        client_name = request.POST.get('client_name')
        client_number = request.POST.get('client_number')
        client_email = request.POST.get('client_email')
        upload_loadschedule = request.FILES.get('upload_loadschedule')
        upload_sld = request.FILES.get('upload_sld')

        errors = {}

        if not (project_code and project_name and consultant and client_name and client_number and client_email):
            errors['all_fields'] = 'All fields are required.'

        if not client_number.isdigit() or len(client_number) != 10:
            errors['client_number'] = 'Invalid client number. Please enter a 10-digit number.'

        if Project.objects.filter(project_code=project_code).exists():
            errors['project_code'] = 'This project code already exists. Please choose a different code.'

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            # Retain form data and redisplay the form with error messages
            return render(request, 'addproject.html', {
                'project_code': project_code,
                'project_name': project_name,
                'consultant': consultant,
                'client_name': client_name,
                'client_number': client_number,
                'client_email': client_email,
            })

        # Create the Project object and save it to the database
        project = Project(
            project_code=project_code,
            project_name=project_name,
            consultant=consultant,
            client_name=client_name,
            client_number=client_number,
            client_email=client_email,
            upload_loadschedule=upload_loadschedule,
            upload_sld=upload_sld
        )
    
        project.save()
        messages.success(request, 'Project added successfully.')
        return redirect('projectlist')  # Redirect to the project list page after successful submission

    return render(request, 'addproject.html')
# todays section
def extract(pdf_path):
    try:
        excel_writer = openpyxl.Workbook()
        excel_writer.remove(excel_writer.active)
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                sheet = excel_writer.create_sheet(title=f'Sheet{page_num + 1}')
                table = page.extract_table()
                if table:
                    for row in table:
                        if row:
                            cleaned_row = [str(cell).strip() if cell is not None else '' for cell in row]
                            if any(cleaned_row):
                                sheet.append(cleaned_row)
    
        # Save the content to an intermediate Excel file
        intermediate_file_path = f"excels/intermediate_{pdf_path}.xlsx"
        excel_writer.save(intermediate_file_path)
        return intermediate_file_path
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        return None

def download_view(request, file_path):
    try:
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
            return response
    except FileNotFoundError:
        return HttpResponse("The file you requested was not found.", status=404)
    




def view_extracted_pdf(request, file_id):
    # Retrieve the file instance from the database
    file_instance = get_object_or_404(Filenew, id=file_id)
    # Check if the file exists
    if file_instance.excel_output_file:
        # Open the extracted Excel file
        with open(file_instance.excel_output_file.path, 'rb') as excel_file:
            # Return the file as a response
            return FileResponse(excel_file, as_attachment=True, filename=file_instance.excel_output_file.name)
    else:
        # Handle the case where the file does not exist
        return HttpResponse("The extracted file does not exist.")   

#todays section







@login_required  
def list(request):
    projects = Project.objects.all()

    # Calculate the serial numbers for each project
    serial_number = 1
    for project in projects:
        project.serial_number = serial_number
        serial_number += 1

    # Split 'projects' into pages with 2 items per page
    paginator = Paginator(projects, 2)
    
    page_number = request.GET.get('page')
    try:
        projects_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        projects_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        projects_page = paginator.page(paginator.num_pages)

    return render(request, 'table.html', {'projects': projects_page})



@login_required
def edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.project_code = request.POST.get('project_code')
        project.project_name = request.POST.get('project_name')
        project.consultant = request.POST.get('consultant')
        project.client_name = request.POST.get('client_name')
        project.client_number = request.POST.get('client_number')
        project.client_email = request.POST.get('client_email')
        project. status=request.POST.get('status')
        # Handle file uploads
        if request.FILES.get('upload_loadschedule'):
            project.upload_loadschedule = request.FILES['upload_loadschedule']
        if request.FILES.get('upload_sld'):
            project.upload_sld = request.FILES['upload_sld']

        project.save()
        messages.success(request, 'Project Edited Successfully')

        response = HttpResponse(request, 'Project details edited successfully.')
        return redirect('projectlist')  # Redirect to the project list page

    context = {'project': project}
    return render(request, 'editproject.html', context)




@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project Deleted Successfully')

        # return HttpResponse('Record Deleted Successfully')
        return redirect('projectlist')  # Redirect to the project list page after deletion
    return redirect('projectlist')  # Redirect to the project list page if GET request or any other method





@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product Deleted Successfully')

        # return HttpResponse('Record Deleted Successfully')
        return redirect('prodlist')  # Redirect to the project list page after deletion
    return redirect('prodlist')  # Redirect to the project list page if GET request or any other method


@login_required
def editpro(request, product_id):
    # Retrieve the product object from the database
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Get the updated data from the form
        product_code = request.POST.get('product_code')
        product_name = request.POST.get('product_name')
        brand_name = request.POST.get('brand_name')
        price_per_unit = request.POST.get('price_per_unit')
        description = request.POST.get('description')
        item_name = request.POST.get('item_name')
        current_rating = request.POST.get('current_rating')
        fault_current = request.POST.get('fault_current')
        power_factor = request.POST.get('power_factor')
        phase = request.POST.get('phase')
        poles = request.POST.get('poles')
        length = request.POST.get('length')
        height = request.POST.get('height')
        width = request.POST.get('width')
        weight = request.POST.get('weight')

        # Update the product object with the new data
        product.product_code = product_code
        product.product_name = product_name
        product.brand_name = brand_name
        product.price_per_unit = price_per_unit
        product.description = description
        product.item_name = item_name
        product.current_rating = current_rating
        product.fault_current = fault_current
        product.power_factor = power_factor
        product.phase = phase
        product.poles = poles
        product.length = length
        product.height = height
        product.width = width
        product.weight = weight

        # Save the updated product object
        product.save()

        messages.success(request, 'Product updated successfully')
        return redirect('prodlist')

    # If the request method is GET, render the edit product form with the existing data
    return render(request, 'editproduct.html', {'product': product})


@login_required
def Reports(request):
    query = request.GET.get('query', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    date_error = None

    # Filter projects based on query and date range
    projects = Project.objects.all()

    if query:
        projects = projects.filter(Q(project_name__icontains=query) | Q(client_name__icontains=query))
    
    if from_date and to_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d')
            projects = projects.filter(project_Date__range=(from_date_parsed, to_date_parsed))
        except ValueError:
            date_error = "Invalid date format. Please use YYYY-MM-DD."

    # Pagination should be applied to the filtered projects queryset
    paginator = Paginator(projects, 2)  # Show 2 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add serial numbers to the projects on the current page
    serial_number = (page_obj.number - 1) * paginator.per_page + 1
    for project in page_obj:
        project.serial_number = serial_number
        serial_number += 1

    return render(request, 'Reports.html', {
        'projects': page_obj,  # Pass the paginated page object
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'date_error': date_error,
        'Reports': page_obj  # Ensure the template can use this for pagination controls
    })

@login_required
def pending(request):
    query = request.GET.get('query', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    date_error = None

    # Filter projects based on query and date range
    projects = Project.objects.filter(status='pending')

    if query:
        projects = Project.objects.filter(Q(project_name__icontains=query) | Q(client_name__icontains=query))
    
    if from_date and to_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d')
            projects =projects.filter(project_Date__range=(from_date_parsed, to_date_parsed))
        except ValueError:
            date_error = "Invalid date format. Please use YYYY-MM-DD."

    # Pagination should be applied to the filtered projects queryset
    paginator = Paginator(projects, 2)  # Show 2 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add serial numbers to the projects on the current page
    serial_number = (page_obj.number - 1) * paginator.per_page + 1
    for project in page_obj:
        project.serial_number = serial_number
        serial_number += 1

    return render(request, 'Reports.html', {
        'projects': page_obj,  # Pass the paginated page object
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'date_error': date_error,
        'Reports': page_obj  # Ensure the template can use this for pagination controls
    })
@login_required
def completed(request):
    query = request.GET.get('query', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    date_error = None

    # Filter projects based on query and date range
    projects = Project.objects.filter(status='completed')

    if query:
        projects = projects.filter(Q(project_name__icontains=query) | Q(client_name__icontains=query))
    
    if from_date and to_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d')
            projects = projects.filter(project_Date__range=(from_date_parsed, to_date_parsed),status='completed')
        except ValueError:
            date_error = "Invalid date format. Please use YYYY-MM-DD."

    # Pagination should be applied to the filtered projects queryset
    paginator = Paginator(projects, 2)  # Show 2 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add serial numbers to the projects on the current page
    serial_number = (page_obj.number - 1) * paginator.per_page + 1
    for project in page_obj:
        project.serial_number = serial_number
        serial_number += 1

    return render(request, 'Reports.html', {
        'projects': page_obj,  # Pass the paginated page object
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'date_error': date_error,
        'Reports': page_obj  # Ensure the template can use this for pagination controls
    })
@login_required
def ongoing(request):
    query = request.GET.get('query', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    date_error = None

    # Filter projects based on query and date range
    projects = Project.objects.filter(status='on-progress')

    if query:
        projects = projects.filter(Q(project_name__icontains=query) | Q(client_name__icontains=query))
    
    if from_date and to_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d')
            projects = projects.filter(project_Date__range=(from_date_parsed, to_date_parsed),status='on-progress')
        except ValueError:
            date_error = "Invalid date format. Please use YYYY-MM-DD."

    # Pagination should be applied to the filtered projects queryset
    paginator = Paginator(projects, 2)  # Show 2 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add serial numbers to the projects on the current page
    serial_number = (page_obj.number - 1) * paginator.per_page + 1
    for project in page_obj:
        project.serial_number = serial_number
        serial_number += 1

    return render(request, 'Reports.html', {
        'projects': page_obj,  # Pass the paginated page object
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'date_error': date_error,
        'Reports': page_obj  # Ensure the template can use this for pagination controls
    })
def projestimate(request):
    return render(request, 'projectdetailsform.html')

