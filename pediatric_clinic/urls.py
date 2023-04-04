from django.urls import path
from . views import *

urlpatterns = [
    path('',home,name='home'),
    # path('booking/', booking_create, name='booking_create'),
    path('Login/',Login_user,name='login'),
    path('user_details/',Admin_view,name='admin_view'),
    path('Vaccinated_view/', Vaccinated_view, name='Vaccinated_view'),
    path('Non_Vaccinated_view/', Non_Vaccinated_view, name='Non_Vaccinated_view'),
    path('Pending_view/', Pending_view, name='Pending_view'),

    path('avaliable_dates/', dates_available, name='avaliable_dates'),

    path('book_vaccine/<int:patient_id>/', book_vaccine, name='book_vaccine'),

    path('add_user/', add_patient, name='add_patient'),
    path('logout/', logout_user, name='logout'),


]
