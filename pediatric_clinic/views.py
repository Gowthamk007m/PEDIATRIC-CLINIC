from django.db.models import Q, F
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Patient, Available_date, Booking
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate,login,logout
from .models import  *
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404
# from .models import Patient


def home(request):
    return render(request, 'index.html')

# def patient_list(request):
#     patients = Patient.objects.all()
#     return render(request, 'patient_list.html', {'patients': patients})


# def patient_detail(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     return render(request, 'patient_detail.html', {'patient': patient})

@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', None)
        phone = request.POST.get('phone')
        birthdate = request.POST.get('birthdate')
        polio_vaccine = request.POST.get('polio_vaccine')

        if polio_vaccine == 'vaccinated':

            polio_vaccine_date = request.POST.get('polio_vaccine_date')
        else:
            polio_vaccine_date = None


        patient = Patient(name=name, email=email, phone=phone, birthdate=birthdate,
                        polio_vaccine=polio_vaccine, polio_vaccine_date=polio_vaccine_date)
        patient.save()

        return redirect('admin_view')

    return render(request, 'add_patient.html')




def Login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_view')
        else:
            return HttpResponse('Invalid login details')
    else:
        # Handle non-POST requests by rendering a login form
        return render(request, 'login1.html')

        
@login_required(login_url='login')
def Admin_view(request):
    data = Patient.objects.all()
    context = {'data': data}
    return render(request, 'patients.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def Vaccinated_view(request):
    data = Patient.objects.filter(polio_vaccine = 'vaccinated')
    context = {'data': data}
    return render(request,'vaccinated.html',context)


@login_required(login_url='login')
def Non_Vaccinated_view(request):
    data = Patient.objects.filter(polio_vaccine='Not vaccinated').exclude(Q(booking__isnull=False) | Q(booking__date__date__lt=datetime.date.today()))

    context = {'data': data}
    return render(request, 'non_vaccinated.html', context)


@login_required(login_url='login')
def Pending_view(request):
    data = Patient.objects.filter(Q(polio_vaccine='pending') | Q(booking__isnull=False)).annotate(
        vaccine_date=F('polio_vaccine_date') or F('booking__date'))

    context = {'data': data}
    return render(request, 'Pending.html', context)


@login_required(login_url='login')
def dates_available(request):
    if request.method == 'POST':
        date = request.POST.get('polio_vaccine_date')
        
        available_date = Available_date.objects.create(date=date)
        available_date.save()
        return redirect('admin_view')
        
    return render(request,'ava_date.html')


# def status(request):


@login_required(login_url='login')
def book_vaccine(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)

    available_dates = Available_date.objects.all()

    if request.method == 'POST':

        selected_date_id = request.POST.get('date')


        selected_date = get_object_or_404(Available_date, pk=selected_date_id)


        booking = Booking(date=selected_date, patient=patient)
        patient.polio_vaccine_date = selected_date.date
        patient.polio_vaccine = 'pending'

        patient.save()

        booking.save()


        return redirect("Non_Vaccinated_view")

    else:
        # Render a template with a form to select the date
        return render(request, 'book_date.html', {'patient': patient, 'available_dates': available_dates})
