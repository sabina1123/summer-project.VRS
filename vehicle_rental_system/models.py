from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    def __str__(self):
     return self.user.username
     
    

class Vehicle(models.Model):
    Type=models.CharField(max_length=20)
    model=models.CharField(max_length=100)
    color=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    RentalRate=models.IntegerField()
    Availability=models.BooleanField()
    image=models.ImageField(upload_to='images/')
    
    def __str__(self):
     return self.model
    
    
class Rental(models.Model):
   
 
    STATUS={
        ("Pending","Pending"),
        ("Ongoing","Ongoing"),
         ("Confirmed","Confirmed") ,
         ("Expired","Expired"),       
    }

    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    RentalStartDateTime=models.DateTimeField()
    RentalEndDateTime=models.DateTimeField()
    TotalCost=models.FloatField()
   
    status=models.CharField(max_length=20,choices=STATUS,default="Pending")    

    