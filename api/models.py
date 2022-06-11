from django.db import models

# Create your models here.

class Citizen(models.Model):
    citizen_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    aadhar = models.CharField(max_length=16)
    dob = models.DateField()
    state = models.CharField(max_length=256)
    pincode = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=256, blank=True, null=True)
    primary_phone = models.CharField(max_length=15)
    other_phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    resume_path = models.CharField(max_length=256, blank=True, null=True)


class CitizenEducationDetails(models.Model):
    citizen = models.ForeignKey('Citizen', on_delete=models.DO_NOTHING, related_name='citizen')
    education_board = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    education_specialization = models.CharField(max_length=255)
    year_of_passing = models.IntegerField()
    institute = models.CharField(max_length=255)
