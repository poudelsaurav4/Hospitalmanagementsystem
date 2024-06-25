from rest_framework import serializers
from hospital.models import *
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib.auth.models import Group, Permission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name', 'email', 'password','address','gender','roles']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name', 'password','email','address','gender','roles']
        # validators  = UniqueValidator('email')

    def validate(self, data):
        if data['username'] == data['first_name']:
            raise serializers.ValidationError({'username':'username cannnot be same as firstname'})
        
        return data
    
    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password  


    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'],
                                                first_name = validated_data['first_name'],
                                                last_name = validated_data['last_name'],
                                                email=validated_data['email'],
                                                password = validated_data['password'],
                                                address = validated_data['address'],
                                                gender = validated_data['gender'],
                                                roles = validated_data['roles']
                                                )
        return user
class DoctorSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'speciality', 'availability'    ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['roles'] = 'doctor'
        user = CustomUser.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id','appointment_date','appointment_time','whatfor' ,'status', 'doctor','patient']


    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(roles='Patient'))
    # def validate(self, data):
    #     doctor = data.get('doctor')
    #     patient = data.get('patient')
        
    #     if doctor and not CustomUser.objects.filter(roles='Doctor').exists():
    #         raise serializers.ValidationError("Selected doctor does not exist.")

    #     return data

    # def create(self, validated_data):
    #     try:
    #         appointment = Appointment.objects.create(
    #             doctor=validated_data['doctor'],
    #             whatfor=validated_data['whatfor'],
    #             appointment_time=validated_data['appointment_time'],
    #             appointment_date = validated_data['appointment_date'],
    #             status=validated_data['status']
    #         )
    #         return appointment
    #     except IntegrityError:
    #         raise serializers.ValidationError("Foreign key constraint failed. Ensure the selected doctorexists.")
    



class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id','patient','doctor','diagnosis','treatment','test_results','progress_notes','date_created']
    
    def create(self, validated_data):
        
        medicalrecord = MedicalRecord.objects.create(
            doctor = validated_data.get('doctor'),
            patient = validated_data.get('patient'),
            diagnosis = validated_data['diagnosis'],
            treatment = validated_data['treatment'],
            test_results = validated_data['test_results'],
            progress_notes = validated_data['progress_notes'],
            date_created = validated_data['date_created']
        )
        return medicalrecord



class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id','patient','doctor','medication', 'dosage','duration','instructions']
    
    def create(self, validated_data):
        prescription = Appointment.objects.create(
            doctor = validated_data.get('doctor'),
            patient = validated_data.get('patient'),
            medication = validated_data['medication'],
            dosage = validated_data['dosage'],
            duration = validated_data['duration'],
            instruction = validated_data['instructions']
      )
        return prescription

