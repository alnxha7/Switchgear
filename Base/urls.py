"""
URL configuration for SwitchGear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #type:ignore
from django.urls import path #type:ignore
from django.contrib.auth import views as auth_views #type:ignore
from . import views
from django.contrib.auth.decorators import login_required # type:ignore
from Base.views import *
from django.conf import settings #type:ignore
from django.conf.urls.static import static #type:ignore


urlpatterns = [
    # path('', views.login, name='login'),  # Assuming this is your custom login view
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Register/', views.reg, name='register'),
    path('Forgot-Password/', views.fp, name='forgotpassword'),
    path('DashBoard/', login_required(views.Dash), name='Dashboard'),
    path('Data_List/', login_required(views.data), name='datalist'),
    path('Location/', login_required(views.loc), name='location'),
    path('New_Project/', login_required(views.addp), name='addproject'),
    path('Project_List/', login_required(views.list), name='projectlist'),
    path('Update_Project/<int:pk>/', login_required(views.edit), name='editproject'),
    path('Reports/', login_required(views.Reports), name='Reports'),
    path('Stafflist/', login_required(views.stafflist), name='stafflist'),
    path('Add_Product/', login_required(views.addprod), name='addprod'),
    path('Product_list/', login_required(views.prodlist), name='prodlist'),
    path('Add-Products/', login_required(views.mulprodlist), name='multiprodlist'),
    path('Change_Password/', login_required(views.changepassword), name='changepswd'),
    path('editstaff/<int:id>/',login_required(views.editstaff), name='editstaff'),  
    path('editlocation/<int:id>/',login_required(views.editloc), name='editlocation'),
    path('Edit_Product/<int:product_id>/', login_required(views.editpro), name='editproduct'),


    path('project/<int:pk>/delete/', login_required(views.delete_project), name='delete_project'),
    path('product/<int:pk>/delete/', login_required(views.delete_product), name='delete_product'),
    path('delstaff/<int:id>/', login_required(views.delstaff), name='delstaff'),
    path('delet/<int:id>/',login_required(views.delet),name='delet'),
    path('on_going',login_required(views.ongoing),name='ongoing'),
    path('compleed',login_required(views.completed),name='completed'),
    path('pending',login_required(views.pending),name='pending'),
    path('Project_Estimate/', login_required(views.projestimate), name='projectestimate'),

    # path('view-extracted-pdf/<int:file_id>/', view_extracted_pdf, name='view_extracted_pdf'), #todays
    # path('fetch-projects/', fetch_projects, name='fetch_projects'),#for fetching projects in reports
    #location validATION URL
    path('check_person_name/',login_required(views.check_person_name),name='check_person_name'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






