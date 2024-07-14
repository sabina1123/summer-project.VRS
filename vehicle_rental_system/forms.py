from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe

class YesNoRadioSelect(forms.widgets.RadioSelect):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.choices = [(True, 'Yes'), (False, 'No')]

    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs=attrs, renderer=renderer)

class AddVehicleForm(forms.ModelForm):
    Type=forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Type", "class":"form-control"}),label="Vehicle Type")
    model=forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Model", "class":"form-control"}),label="Model")
    color=forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Color", "class":"form-control"}),label=" Color")
    description = forms.CharField(label='Vehicle Description', widget=forms.Textarea(attrs={"placeholder":"Description","class":"form-control"}))
    RentalRate=forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"RentalRate", "class":"form-control"}),label="Rental Rate")
    Availability = forms.BooleanField(required=True,widget=YesNoRadioSelect(attrs={"class": "form-control"}),label="Availability")
    
    class Meta:
        model=Vehicle
        exclude=("user",)
        
        





class AddCustomerForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Your Username", "class": "form-control"}), label="Username")
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password", "class": "form-control"}), label="Password")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter Your Email", "class": "form-control"}), label="Email")
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Your Phone Number", "class": "form-control"}), label="Phone Number")
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Your Address", "class": "form-control"}), label="Address")
    

    class Meta:
        model = Customer
        fields = ['username', 'password','email', 'phone', 'address']
    
    # def __init__(self, *args, **kwargs):
    #     self.instance = kwargs.get('instance')
    #     super(AddCustomerForm, self).__init__(*args, **kwargs)

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if self.instance and self.instance.username == username:
    #         return username
    #     if Customer.objects.filter(username=username).exists():
    #         raise forms.ValidationError("This username is already taken. Please choose a different one.")
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if self.instance and self.instance.email == email:
    #         return email
    #     if Customer.objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already registered. Please use a different email address.")
    #     return email

    # def __init__(self, *args, **kwargs):
    #     customer = kwargs.pop('instance', None)
    #     super(AddCustomerForm, self).__init__(*args, **kwargs)
    #     if customer and customer.user:
    #         self.fields['username'].initial = customer.user.username
    #         self.fields['email'].initial = customer.user.email

    
    
 

        

class BookingForm(forms.Form):

    customer = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    vehicle = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    RentalStartDateTime = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    RentalEndDateTime = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    TotalCost=forms.FloatField( widget=forms.TextInput(attrs={"placeholder": "Total Cost", "class": "form-control","readonly":"readonly" }), label="Total Cost" )
    
    price_per_day = forms.FloatField(widget=forms.HiddenInput())

    
    class Meta:
        model = Rental
        exclude = ("customer",)
        
    def __init__(self, *args, **kwargs):
        customer_id = kwargs.pop('customer_id', None)
        vehicle_id = kwargs.pop('vehicle_id', None)
        price_per_day = kwargs.pop('price_per_day', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if customer_id:
            self.fields['customer'].initial = customer_id
        if vehicle_id:
            self.fields['vehicle'].initial = vehicle_id
        if price_per_day:
           self.fields['price_per_day'].initial = price_per_day
            
            
class CustomPasswordChangeForm(PasswordChangeForm):
    def save(self, commit=True):
        user = super().save(commit=commit)
        # Update the Customer model if necessary
        if commit:
            customer = Customer.objects.get(user=user)
            customer.password_updated_at = timezone.now()  # Example field to track password update
            customer.save()
        return user
    
    
class VehicleSearchForm(forms.Form):
    model = forms.CharField(required=False, max_length=100)
    
    
# class EditRentalForm(forms.Form):
#     STATUS=(
#         ("Pending","Pending"),
#         ("Ongoing","Ongoing"),
#         ("Confirm","Confirm") ,
#         ("Expired","Expired")       
#       )
#     status=payment_method = forms.ChoiceField(choices=STATUS, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
#     class Meta:
#         model = Rental
#         fields = ['status']
class EditRentalForm(forms.ModelForm):
    STATUS = (
        ("Pending", "Pending"),
        ("Ongoing", "Ongoing"),
        ("Confirmed", "Confirmed"),
        ("Expired", "Expired"),       
    )
    
    status = forms.ChoiceField(choices=STATUS, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Rental
        fields = ['status']