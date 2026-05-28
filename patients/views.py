from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm
from .services import generate_health_remark
from django.contrib import messages

# Create your views here.

def home(request):

    search_query = request.GET.get('search', '')

    patients = Patient.objects.filter(
        full_name__icontains=search_query
    )

    total_patients = patients.count()

    high_risk = patients.filter(
        remarks__icontains='High risk'
    ).count()

    normal = patients.filter(
        remarks__icontains='normal'
    ).count()

    return render(request, 'home.html', {

        'patients': patients,
        'search_query': search_query,

        'total_patients': total_patients,
        'high_risk': high_risk,
        'normal': normal,
    })

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.remarks = generate_health_remark(
                patient.glucose,
                patient.haemoglobin,
                patient.cholesterol
            )

            patient.save()
            messages.success(
                request,
                "Patient added successfully."
            )

            return redirect('home')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {
            'form': form
        })

def edit_patient(request, id):

    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.remarks = generate_health_remark(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

        patient.save()
        messages.success(
            request,
            "Patient updated successfully."
        )

        return redirect('home')

    else:
        form = PatientForm(instance=patient)
        return render(request, 'add_patient.html', {
            'form': form
        })

def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(
        request,
        "Patient deleted successfully."
    )
    return redirect('home')