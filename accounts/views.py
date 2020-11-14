from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *  # To make available the models and all its variables
# available to products.html file so that all the products in the database can
# be shown in the webpage.
# Create your views here.
from .forms import *
from django.forms import inlineformset_factory
from .filters import ActivityFilter
from django.contrib import messages
# Flash messages are way of sending one time message to the templates.
from django.contrib.auth import authenticate, login, logout
# authenticate to check if a user is in the DB
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
import re


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Only username without any other thing is grabbed by the above cleaned data
            
            messages.success(request, 'Account creation for '+username+' is successful!')
            return redirect('login')

    s = form.errors
    k = list(s.keys())
    v = list(s.values())
    print(k, v)
    err_list = []
    if k:
        err = True
        if 'username' in k:
            p = ['A user with that username already exists.']
            if p in v:
                err_list.append(p[0])
            else:
                err_list.append('Please provide a username' )
        if 'password1' or 'password2' in k:
            err_list.append('Passwords don\'t match')
        err_list.append('Both username and password are case-sensitive. Verify your credentials.')
    else:
        err = False
    context = {
        'form': form,
        'err': err,
        'err_list': err_list,
    }
    return render(request,'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Those above are obtained from the input fields in the login.html
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and/or password are/is incorrect!')
    context = {}
    return render(request,'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    activities = Activity.objects.all()
    patients = Patient.objects.all()
    total_patients = patients.count()
    total_activities = activities.count()
    opf = activities.filter(status='OPF').count()
    upf = activities.filter(status='UPF').count()
    context = {
        'activities': activities[::-1],
        'patients': patients,
        'total_activities': total_activities,
        'total_patients': total_patients,
        'opf': opf,
        'upf': upf,
        'opf_ratio': str(opf/total_activities)+'%',
        'upf_ratio': str(upf/total_activities)+'%',
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'customer',
])
def userPage(request):
    activities = request.user.patient.activity_set.all()

    total_activities = activities.count()
    opf = activities.filter(status='OPF').count()
    upf = activities.filter(status='UPF').count()

    print('ORDERS: ', activities)
    context = {
        'activities': activities,
        'total_activities': total_activities,
        'opf': opf,
        'upf': upf,
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'customer',
    'top_customer',
])
def accountSettings(request):
    patient = request.user.patient
    form = PatientForm(instance=patient)
    group = [x.name for x in request.user.groups.all()]
    if 'top_customer' in group:
        top = True
    else:
        top = False
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()


    context = {
        'form': form,
        'top': top,
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'admin',
])
def products(request):
    games = Game.objects.all()
    return render(request, 'accounts/products.html', {
        'games': games,
    })

@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'admin',
])
def customer(request, pk):
    patient = Patient.objects.get(id=pk)
    print(patient)
    activities = patient.activity_set.all() # CAUTION
    total_activities = activities.count()
    my_filter = ActivityFilter(request.GET, queryset=activities)
    # print(my_filter.form)
    activities = my_filter.qs
    context = {
        'patient': patient,
        'activities': activities,
        'total_activities': total_activities,
        'my_filter': my_filter,
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'admin',
])
def createOrder(request, primary_key_):
    ActivityFormSet = inlineformset_factory(Patient, Activity, fields=(
        'game',
        'status',
    ), extra = 10)  # extra = 10 creates 10 fields for placing order
    patient = Patient.objects.get(id=primary_key_)
    # form = OrderForm(initial={
    #     'customer':customer,
    # })
    formset = ActivityFormSet(queryset=Activity.objects.none(),instance=patient)
    # The queryset Order.objects.none() => If we already have objects don't show them because we are "Placing Order"
    if request.method == 'POST':
        # form = ActivityForm(request.POST)
        formset = ActivityFormSet(request.POST, instance=patient)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'form': formset,
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'admin',
])
def updateOrder(request, primary_key_):
    activity = Activity.objects.get(id=primary_key_)
    # print(activity)
    form = ActivityForm(instance=activity)  # To pre-fill with old order that is to be updated now
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[
    'admin',
])
def deleteOrder(request, primary_key_):
    activity = Activity.objects.get(id=primary_key_)
    if request.method == 'POST':
        activity.delete()  # Delete function provided by Django
        return redirect('/')
    context = {
        'item': activity,
    }
    return render(request, 'accounts/delete.html', context)
