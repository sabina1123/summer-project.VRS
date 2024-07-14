from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect, Http404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from .forms import AddVehicleForm,AddCustomerForm,BookingForm,CustomPasswordChangeForm,VehicleSearchForm,EditRentalForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse
import requests as req
import hashlib
import uuid
import hmac
import base64
from django.core.mail import send_mail
from django.core.paginator import Paginator


#Create your views here.

def profile(request):
    customer = get_object_or_404(Customer, email=request.user.email)

    return render(request,'profile.html',{'customer':customer})





def customerBooking(request):
    customer = get_object_or_404(Customer, email=request.user.email)
    rentals = Rental.objects.filter(customer_id=customer.id).select_related('vehicle')
    vehicle_rentals = []
    for rental in rentals:
        vehicle_rentals.append({
            'vehicle': rental.vehicle,
            'rental': rental
        })

    return render(request, 'customer_booking.html', {'vehicle_rentals': vehicle_rentals})
   

    
def home(request):
    vehicles=Vehicle.objects.all()
    
    return render(request,'home.html',{'vehicles':vehicles})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
               
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, "Registration Successful.")
            return redirect('user_login')
    else:
        form = AddCustomerForm()
    return render(request, 'signup.html', {'form': form})




# @login_required
# def change_password(request):
#     customer=get_object_or_404(Customer,email=request.user.email)
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  
#             customer.password = request.user.password
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = CustomPasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})
@login_required
def change_password(request):
    customer = get_object_or_404(Customer, email=request.user.email)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            customer.password = user.password  # Update Customer's password
            customer.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})
        


def Contact(request):
    if request.method == 'POST':
       
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
			name,
			message, 
			email, 
			['gracefuladventure4@gmail.com'], 
			)
        return render(request, 'contact.html', {'name':name})
 
    else:
      return render(request,'contact.html')



def book_vehicle(request):
    vehicles=Vehicle.objects.all()
    
    paginator=Paginator(vehicles,9)
    page_number=request.GET.get('page')
    vehiclesfinal=paginator.get_page(page_number)
    totalpage=vehiclesfinal.paginator.num_pages
    
    
    data={
        'vehicles': vehiclesfinal,
        'lastpage':totalpage,
        'totalPagelist':[n+1 for n in range(totalpage)]
    }
    
    return render(request,'book_vehicle.html',data)



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"You Have Been Logged In!")
            return redirect('/dashboard/')
        else:
            messages.success(request,"There was An Error Logging In, Please Try Again !!!")
            return redirect('login')
        
    else:
        return render(request,'login.html')

        
def admin_logout(request):
    logout(request)
    messages.success(request,"You Have Been Logged Out")
    return redirect('/admin_login/')


    
@login_required(login_url="/admin_login/")  
def dashboard(request):
    return redirect('admin_dashboard')



@login_required(login_url="/admin_login/")
def Vehicle_list(request):
    vehicles = Vehicle.objects.all()
    
    return render(request, 'vehicle.html',{'vehicles':vehicles})




@login_required(login_url="/admin_login/")
def add_vehicle(request):
    form = AddVehicleForm(request.POST,request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST":
           if form.is_valid():
                add_record=form.save()
                messages.success(request,"Vehicle Added..")
                return redirect('vehicle_list')
        else:
             form = AddVehicleForm()  
        return render(request,'add_vehicle.html',{'form':form})
           
    else:
        messages.success(request,"You Must Be Logged In..")
        return redirect('login')
  
  
    
@login_required(login_url="/admin_login/")        
def delete_vehicle(request,id):
    vehicle=Vehicle.objects.get(id=id) 
    vehicle.delete()
    messages.success(request,"Vehicle Deleted..")
    return redirect('/dashboard/vehicle/')  



@login_required(login_url="/admin_login/") 
def edit_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddVehicleForm(request.POST, request.FILES, instance=vehicle)
            if form.is_valid():
                form.save()
                messages.success(request, "Vehicle updated successfully.")
                return redirect('vehicle_list')
            else:
                messages.error(request, "There was an error updating the vehicle.")
        else:
            form = AddVehicleForm(instance=vehicle)
        return render(request, 'edit_vehicle.html', {'form': form, 'vehicle': vehicle})
    else:
        messages.error(request, "You must be logged in to edit a vehicle.")
        return redirect('login')
    
    
    
    
@login_required(login_url="/admin_login/")    
def Customer_list(request):
    customers=Customer.objects.all()
    
    return render(request,'customer.html',{'customers':customers})




@login_required(login_url="/admin_login/")
def add_customer(request):
    form = AddCustomerForm(request.POST)
    if request.user.is_authenticated:
        if request.method == "POST":
           if form.is_valid():
                add_record=form.save()
                messages.success(request,"Customer Added..")
                return redirect('customer_list')
        else:
             form = AddCustomerForm()  
        return render(request,'add_customer.html',{'form':form})
           
    else:
        messages.success(request,"You Must Be Logged In..")
        return redirect('login')
    
    
    
    
@login_required(login_url="/admin_login/")   
def delete_customer(request,id):
    customers=Customer.objects.get(id=id)
    customers.delete()
    messages.success(request,"Customer Deleted..")
    return redirect('/dashboard/customer/')



@login_required(login_url="/user_login/")

def edit_customer(request):
    customer = get_object_or_404(Customer, email=request.user.email)

    if request.method == "POST":
        form = AddCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            try:
            
                user = request.user
                updated = False
                if user.username != customer.username:
                    user.username = customer.username
                    updated = True
                if user.email != customer.email:
                    user.email = customer.email
                    updated = True
                if updated:
                   user.save()
                messages.success(request, "Customer updated successfully.")
                return redirect('profile') 
            except User.DoesNotExist:
                messages.error(request, "Associated user not found.")
                return redirect('profile')  
        else:
            messages.error(request, "There was an error updating the customer.")
            print(form.errors)  
    else:
        form = AddCustomerForm(instance=customer)

    return render(request, 'edit_customer.html', {'form': form})



def book_detail(request, id):
    vehicle = Vehicle.objects.get(id=id) 
    return render(request,'book.html',{'vehi':vehicle})  

 







@login_required(login_url="/admin_login/")
def rental(request):
    rentals=Rental.objects.all()
    for rent in rentals:
      print(rent) 
    return render(request,'Rental.html',{'rentals':rentals})

# @login_required(login_url="/admin_login/")
# def delete_rental(request,id):
#     rentals=Rental.objects.get(id=id)
#     rentals.delete()
#     messages.success(request,"Booked Deleted..")
#     return redirect('/dashboard/rental/')

# @login_required(login_url="/admin_login/")
# def edit_rental(request, id):
#     rental = get_object_or_404(Rental, id=id)
    
#     if request.method == 'POST':
#         form = EditRentalForm(request.POST, instance=rental)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard/rental', id=id)
#     else:
#         form = EditRentalForm(instance=rental)
    
#     return render(request, 'edit_rental.html', {'form': form})
@login_required(login_url="/admin_login/")
def edit_rental(request, id):
    rental = get_object_or_404(Rental, id=id)
    
    if request.method == 'POST':
        form = EditRentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/rental/', id=id)
    else:
        form = EditRentalForm(instance=rental)
    
    return render(request, 'edit_rental.html', {'form': form})
    
    
    
    
 

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=User.objects.get(email=email).username, password=password)
    
        if user is not None:
            login(request, user)
            customer = Customer.objects.get(email=email)
            request.session['customer_id'] = customer.id
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials !!!")
            return redirect('user_login')
    else:
        return render(request, 'user_login.html')



def user_logout(request):
    logout(request)
    messages.success(request,"You Have Been Logged Out")
    return redirect('/')

 


# ESEWA_MERCHANT_ID = 'YOUR_ESEWA_MERCHANT_ID'
# ESEWA_SUCCESS_URL = 'http://localhost:8000/payments/success/'
# ESEWA_FAILURE_URL = 'http://localhost:8000/payments/failure/'



@login_required(login_url="/user_login/")
def initiate_booking(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    price_per_day=vehicle.RentalRate
    
    if request.method == 'POST':
        form = BookingForm(request.POST,price_per_day=price_per_day)
        if form.is_valid():
            customer_id = request.session.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id)
            

            rental = Rental(
                customer=customer,
                vehicle=vehicle,
                RentalStartDateTime=form.cleaned_data['RentalStartDateTime'],
                RentalEndDateTime=form.cleaned_data['RentalEndDateTime'],
                TotalCost=form.cleaned_data['TotalCost'],
          
            )
            rental.save()

            messages.success(request, "Booked Successfully...")
            return redirect('book_vehicle')
    else:
        form = BookingForm(customer_id=request.session.get('customer_id'), vehicle_id=vehicle.id, price_per_day=price_per_day)

    return render(request, 'initiate_booking.html', {'form': form, 'vehi': vehicle})

def payment_success(request):
    ref_id = request.GET.get('refId')
    oid = request.GET.get('oid')
    amt = request.GET.get('amt')
    if ref_id and oid and amt:
        rental = Rental.objects.filter(id=oid, TotalCost=amt).first()
        if rental:
            rental.status = 'COMPLETED'
            rental.save()
            return render(request, 'payments/success.html', {'rental': rental})
    return redirect('payment_failure')

def payment_failure(request):
    return render(request, 'payments/failure.html')


def search(request):
   query=request.GET['query']
   vehicle=Vehicle.objects.filter(model__icontains=query)
   params={'vehicle':vehicle}
   return render(request,'search.html',params)

def is_admin(user):
    return user.is_superuser

@login_required(login_url="/admin_login/")
def admin_dashboard(request):
    total_customers = Customer.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_admins = User.objects.filter(is_superuser=True).count()

    context = {
        'total_customers': total_customers,
        'total_vehicles': total_vehicles,
        'total_admins': total_admins,
    }

    return render(request, 'admin_dashboard.html', context)
