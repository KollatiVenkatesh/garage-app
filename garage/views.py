from django.shortcuts import render, redirect
from .models import Vehicle, Visit
from .forms import VehicleForm, VisitForm
from .forms import CustomerForm
from .models import RepairJob
from .forms import RepairJobForm

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Customer, Vehicle
from .forms import CustomerForm, VehicleForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import RepairJob
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    # ======================
    # CUSTOMER LOGIC
    # ======================
    search_query = request.GET.get('search', '')

    customers = Customer.objects.all().order_by('-id')

    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    edit_id = request.GET.get('edit_id')
    instance = None

    if edit_id:
        instance = get_object_or_404(Customer, id=edit_id)

    form = CustomerForm(request.POST or None, instance=instance)

    if request.method == 'POST' and 'customer_submit' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('/?tab=customer')


    # ======================
    # VEHICLE LOGIC (ADD THIS)
    # ======================
    vehicle_qs = Vehicle.objects.all().order_by('-id')

    vehicle_paginator = Paginator(vehicle_qs, 10)
    vehicle_page_number = request.GET.get('vehicle_page')
    vehicle_page_obj = vehicle_paginator.get_page(vehicle_page_number)

    vehicle_edit_id = request.GET.get('vehicle_edit_id')
    vehicle_instance = None

    if vehicle_edit_id:
        vehicle_instance = get_object_or_404(Vehicle, id=vehicle_edit_id)

    vehicle_form = VehicleForm(request.POST or None, instance=vehicle_instance)

    if request.method == 'POST' and 'vehicle_submit' in request.POST:
        if vehicle_form.is_valid():
            vehicle_form.save()
            return redirect('/?tab=vehicle')

    # VISIT LOGIC

    visit_qs = Visit.objects.all().order_by('-id')

    visit_paginator = Paginator(visit_qs, 10)
    visit_page_number = request.GET.get('visit_page')
    visit_page_obj = visit_paginator.get_page(visit_page_number)

    visit_edit_id = request.GET.get('visit_edit_id')
    visit_instance = None

    if visit_edit_id:
        visit_instance = get_object_or_404(Visit, id=visit_edit_id)

    visit_form = VisitForm(request.POST or None, instance=visit_instance)

    if request.method == 'POST' and 'visit_submit' in request.POST:
        if visit_form.is_valid():
            visit_form.save()
            return redirect('/?tab=visit')

    # VEHICLE HISTORY

    history_vehicle = None
    history_page_obj = None
    history_visits = []

    search_number = request.GET.get('vehicle_search')

    if search_number:
        try:
            history_vehicle = Vehicle.objects.get(number_plate__iexact=search_number)
            history_qs = Visit.objects.filter(vehicle=history_vehicle).order_by('-created_at')

            history_paginator = Paginator(history_qs, 10)
            history_page_number = request.GET.get('history_page')
            history_page_obj = history_paginator.get_page(history_page_number)
        except Vehicle.DoesNotExist:
            history_vehicle = None


    # ======================
    # FINAL RETURN
    # ======================
    return render(request, 'dashboard.html', {
        'form': form,
        'customers': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'edit_id': edit_id,

        'vehicle_form': vehicle_form,
        'vehicles': vehicle_page_obj,
        'vehicle_page_obj': vehicle_page_obj,
        'vehicle_edit_id': vehicle_edit_id,

        'visit_form': visit_form,
        'visits': visit_page_obj,
        'visit_page_obj': visit_page_obj,
        'visit_edit_id': visit_edit_id,

        'history_vehicle': history_vehicle,
        'history_visits': history_page_obj,
        'history_page_obj': history_page_obj,
        'search_number': search_number,
    })

def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('dashboard')

def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    vehicle.delete()
    return redirect('/?tab=vehicle')

def delete_visit(request, id):
    visit = get_object_or_404(Visit, id=id)
    visit.delete()
    return redirect('/?tab=visit')

def add_repair(request, visit_id):
    form = RepairJobForm(request.POST or None)

    if form.is_valid():
        repair = form.save(commit=False)
        repair.visit_id = visit_id
        repair.save()
        return redirect('vehicle_history', vehicle_id=repair.visit.vehicle.id)

    return render(request, 'add_repair.html', {'form': form})

def add_customer(request):
    form = CustomerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'partials/customer_form.html', {'form': form})

def add_vehicle(request):
    form = VehicleForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'partials/vehicle_form.html', {'form': form})

def add_visit(request):
    form = VisitForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'partials/visit_form.html', {'form': form})

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

def update_status(request, job_id):
    job = get_object_or_404(RepairJob, id=job_id)

    if job.status == 'Pending':
        job.status = 'Completed'
    else:
        job.status = 'Pending'

    job.save()

    return redirect(request.META.get('HTTP_REFERER'))

def vehicle_history(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    visits = Visit.objects.filter(vehicle=vehicle)

    return render(request, 'vehicle_history.html', {
        'vehicle': vehicle,
        'visits': visits
    })


from django.core.paginator import Paginator
