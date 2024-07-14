from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_title = 'Vehicle Rental System'
admin.site.site_header = 'Vehicle Rental System'
admin.site.index_title = 'Vehicle Rental System'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields=('username',)
    list_display=('username','password','email','phone','address',)
    list_per_page=10
    
    
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    search_field=('Type',)
    list_display=('Type','model','color','RentalRate','Availability','image',)
    list_per_page=10
    
    
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display=('customer','vehicle','RentalStartDateTime','RentalEndDateTime','TotalCost','status',)
    list_per_page=10
    list_filter=('customer','vehicle',)
    
    
    
    
    
