from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import *


router = DefaultRouter()
router.register(r'registeruser', Register, basename='register')
router.register(r'patient', PatientView, basename='patient')
router.register(r'appointment', DocAppointment, basename='appointment')
router.register(r'medrecord', PatientMedicalRecord, basename='medrecord')
router.register(r'prescription', DocPrescription, basename='prescription')


urlpatterns = [
    path('', include(router.urls)),
    path('doctors/', DoctorCreateView.as_view(), name='doctor-create'),

]