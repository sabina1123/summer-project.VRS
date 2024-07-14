from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
# from .views import EsewaRequestView



urlpatterns = [
    path('admin_login/',admin_login,name="admin_login"),
    path('admin_logout/',admin_logout),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard/vehicle/',Vehicle_list,name="vehicle_list"),
    path('dashboard/vehicle/add_vehicle/',add_vehicle,name="add_vehicle"),
    path('vehicle/<int:id>/delete_vehicle/',delete_vehicle,name="delete_vehicle"),
    path('dashboard/vehicle/<int:id>/edit_vehicle/',edit_vehicle,name="edit_vehicle"),
    path('dashboard/customer/',Customer_list,name="customer_list"),
    path('dashboard/customer/add_customer/',add_customer,name="add_customer"),
    path('dashboard/customer/<int:id>/delete_customer/',delete_customer,name="delete_customer"),
    # path('dashboard/customer/<int:id>/edit_customer/',edit_customer,name="edit_customer"),
    path('update/',edit_customer,name="edit_customer"),
    path('',home,name="home"),
    path('book_vehicle/',book_vehicle,name="book_vehicle"),
    path('book/<int:id>/',book_detail,name="book_detail"),
    path('book/<int:id>/initiate_booking/',initiate_booking,name="initiate_booking"),
    path('dashboard/rental/',rental,name="rental"),
    path('dashboard/rental/<int:id>/edit_rental/',edit_rental,name="edit_rental"),
    # path('dashboard/rental/<int:id>/delete_rental/',delete_rental,name="delete_rental"),
    # path('profile_list/',profile_list,name="profile_list"),
    path('profile/',profile ,name="profile"),
    path('user_login/',user_login,name="user_login"),
    path('user_logout/',user_logout,name="user_logout"),
    path('signup/',signup,name="signup"),
    # path('select_vehicle/<int:vehicle_id>/', select_vehicle, name='select_vehicle'),
    # path("esewa_request/",EsewaRequestView.as_view(),name="verify_esewa"),
    path('initiate_booking/<int:id>/', initiate_booking, name='initiate_booking'),
    # path('payments/success/', payment_success, name='payment_success'),
    # path('payments/failure/', payment_failure, name='payment_failure'),
    path('customerbooking/',customerBooking,name='customerbooking'),
    path('change-password/', change_password, name='change_password'),
    path('search',search,name="search"),
    path('contact/',Contact,name="contact"),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

