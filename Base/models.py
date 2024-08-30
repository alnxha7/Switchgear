from django.db import models #type:ignore
from django.contrib.auth.models import User #type:ignore
from django.core.validators import FileExtensionValidator #type:ignore
# from django.core.validators import RegexValidator #type:ignore
from django.core.exceptions import ValidationError #type:ignore
from django.utils.translation import gettext_lazy as _  #type:ignore
from django.contrib.auth.models import AbstractUser #type:ignore
from django.contrib.auth.hashers import make_password #type:ignore
#for staff registration
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager #type:ignore

def validate_mobile_number(value):
    if not value.startswith('+'):
        raise ValidationError(_('Mobile number must start with +'))
    if len(value) < 10 or len(value) > 15:
        raise ValidationError(_('Mobile number must be between 10 and 15 characters'))



class Project(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('on-progress', 'On Progress'),
        ('completed', 'Completed'),
    )
    
    project_code = models.CharField(max_length=50,unique=True)
    project_name = models.CharField(max_length=255)
    consultant = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_number = models.CharField(
        max_length=15,validators=[validate_mobile_number]
    )
    client_email = models.EmailField()
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    upload_loadschedule = models.FileField(
      upload_to='pdf/',
      validators=[FileExtensionValidator(['pdf'])],  # Restrict to PDF files
      help_text='Upload PDF file only'  # Optional help text for the field
    )   # Optional help text for the field
    upload_sld = models.ImageField(upload_to='sld/')
    project_Date = models.DateField(auto_now=True)

    def __str__(self):
        return self.project_name


    


class Product(models.Model):
    PRODUCT_PHASE_CHOICES = [
        ('Three Phase', 'Three Phase'),
        ('Single Phase', 'Single Phase'),
    ]

    POLE_CHOICES = [
        ('3 Pole', '3 Pole'),
        ('4 Pole', '4 Pole'),
    ]

    product_code = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    current_rating = models.IntegerField(blank=True, null=True)
    fault_current = models.IntegerField( blank=True, null=True)
    power_factor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    phase = models.CharField(max_length=20, choices=PRODUCT_PHASE_CHOICES, blank=True, null=True)
    poles = models.CharField(max_length=20, choices=POLE_CHOICES, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def _str_(self):
        return self.product_name
    


class Filenew(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/') 
    sld_file = models.FileField(upload_to='slds/', null=True, blank=True) 
    data_from_sld = models.FileField(upload_to='slds/', null=True, blank=True) 
    excel_intermediate_file = models.FileField(upload_to='excels/', null=True, blank=True)
    excel_output_file = models.FileField(upload_to='excels/', null=True, blank=True)
    
    def _str_(self):
        return f"File ID: {self.id}, PDF: {self.pdf_file.name}"
    
class MultiProduct(models.Model):    
    multi_products = models.FileField(upload_to='products/' )
    data_from_multi_products = models.FileField(upload_to='products/', null=True, blank=True)
   
# class Employee (models.Model):
#     userid=models.ForeignKey(User,on_delete=models.CASCADE)
#     empcode=models.CharField(max_length=100,)
#     designation=models.CharField(max_length=200,)
#     address=models.CharField(max_length=400,)
#     contact=models.IntegerField()

class Employee1 (models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    empcode=models.CharField(max_length=100,)
    designation=models.CharField(max_length=200,)
    name =models.CharField(max_length=250)
    address=models.CharField(max_length=400,)
    contact=models.IntegerField()
    email=models.CharField(max_length=200)
    uname=models.CharField(max_length=200)
    passwrd=models.CharField(max_length=200)
    
    
class Location(models.Model):
    locationname=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    
    
class LocationTax(models.Model):
    locationid=models.ForeignKey(Location,on_delete=models.CASCADE) 
    taxpercentage=models.CharField(max_length=255)
    def __str__(self):
        return self.taxpercentage
    

class SearchRecord(models.Model):
    pole = models.CharField(max_length=255)
    mccb = models.IntegerField()
    fault_duty = models.IntegerField()
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'POLE: {self.pole}, MCCB: {self.mccb}, FAULT DUTY: {self.fault_duty}'


    