from django.db import models

# Create your models here.
class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    otp = models.IntegerField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    profilepic = models.ImageField(upload_to="app/img/candidate")

class Company(models.Model):
    user_id = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    companyname = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    logopic = models.ImageField(upload_to="app/img/company")

# job details
class JobDetails(models.Model):
    comp_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    jobname = models.CharField(max_length=250)
    companyname = models.CharField(max_length=250)
    companyaddress = models.CharField(max_length=250)
    jobdesc = models.TextField(max_length=500)
    qualification = models.CharField(max_length=250)
    responsibility = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    website = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    salary = models.CharField(max_length=250)
    experience = models.CharField(max_length=50)

class ApplyJob(models.Model):
    job_id = models.ForeignKey(JobDetails,on_delete=models.CASCADE)
    can_id = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    contact = models.CharField(max_length=50,default="")
    state = models.CharField(max_length=50,default="")
    city = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=50,default="")
    gender = models.CharField(max_length=10,default="")
    website = models.CharField(max_length=50,default="")
    min_salary = models.CharField(max_length=5,default="")
    max_salary = models.CharField(max_length=10,default="")
    experience = models.CharField(max_length=5,default="")
    education = models.CharField(max_length=10,default="")
    