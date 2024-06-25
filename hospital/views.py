from django.shortcuts import render
from rest_framework import viewsets, mixins,generics
from .models import *
from .serializers import *
# Create your views here.



class Register(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DocAppointment(viewsets.ModelViewSet):
    queryset= Appointment.objects.all()
    serializer_class = AppointmentSerializer

    
class PatientMedicalRecord(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

class DocPrescription(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

