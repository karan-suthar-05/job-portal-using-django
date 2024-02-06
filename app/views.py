from django.shortcuts import render,redirect
from .models import *
from random import *
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# for sending email
def sendOtp(email):
    subject = "OTP Verification!!!"
    otp = randint(100000,999999)
    message = f"OTP-{otp} for job portal website."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    return otp

def resendOtp(request,email):
    otp = sendOtp(email)
    request.session["otp"] = otp
    return render(request,'app/otpverify.html')    
def indexPage(request):
    return render(request,"app/index.html")

def signupPage(request):
    return render(request,"app/signup.html")

def registerUser(request):
    role = request.POST["role"]
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    user = UserMaster.objects.filter(email=email)
    request.session["otpemail"] = email
    if user:
        msg = "User already exist!!"
        return render(request,"app/signup.html",{"msg":msg})
    else:
        if request.POST['role']=="Candidate":
                if password==cpassword:
                    otp = randint(100000,999999)
                    otp = sendOtp(email)
                    request.session["otp"] = otp
                    newuser = UserMaster.objects.create(role=role,email=email,password=password,otp=otp)
                    newcand = Candidate.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                    return render(request,"app/otpverify.html",{"email":email})
                else:
                    msg = "Password and confirm password doesn't match"
                    return render(request,"app/signup.html",{"msg":msg})
        else:
                if password==cpassword:
                    otp = randint(100000,999999)
                    otp = sendOtp(email)
                    request.session["otp"] = otp
                    newuser = UserMaster.objects.create(role=role,email=email,password=password,otp=otp)
                    newcomp = Company.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                    return render(request,"app/otpverify.html",{"email":email})
                else:
                    msg = "Password and confirm password doesn't match"
                    return render(request,"app/signup.html",{"msg":msg})

def otpPage(request):
    return render(request,"app/otpverify.html")

def otpVerification(request):
    if request.method == "POST":
        email = request.POST["email"]
        otp = int(request.POST['otp'])
        user = UserMaster.objects.get(email=email)
        if request.session["otp"] == otp:
            request.session.flush()
            msg = "otp verification successfull."
            return render(request,"app/login.html",{"msg":msg})
        else:
            msg = "otp verification fail!!"
            return render(request,"app/otpverify.html",{"msg":msg,"email":email})

def loginPage(request):
    return render(request,"app/login.html")

def login(request):
    role = request.POST["role"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = UserMaster.objects.get(email=email)
    if user:
            if password==user.password:
                request.session["id"] = user.id
                request.session["role"] = user.role
                request.session["email"] = user.email
                request.session["password"] = user.password
                if role=="Candidate":
                    can = Candidate.objects.get(user_id=user)
                    request.session["firstname"] = can.firstname
                    request.session["lastname"] = can.lastname
                    return redirect("indexPage")
                else:
                    comp = Company.objects.get(user_id=user)
                    request.session["firstname"] = comp.firstname
                    request.session["lastname"] = comp.lastname
                    return redirect("compIndex")
            else:
                msg = "password is wrong"
                return render(request,"app/login.html",{"msg":msg})
    else:
        msg = "user doesn't exist!!"
        return render(request,"app/login.html",{"msg":msg})

# profile data geting page
def profileDetails(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == 'Candidate':
        role = Candidate.objects.get(user_id=user)
    else:
        role = Company.objects.get(user_id=user)
    return render(request,"app/registration.html",{'user':user,'role':role})

def updateProfile(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role=="Candidate":
        can = Candidate.objects.get(user_id=user)
        can.firstname = request.POST['fname']
        can.lastname = request.POST['lname']
        can.state = request.POST['state']
        can.city = request.POST['city']
        can.contact = request.POST['phone']
        can.address = request.POST['address']
        can.dob = request.POST['dob']
        can.gender = request.POST['gender']
        can.profilepic = request.FILES['pp']
        can.save()
    else:
        comp = Company.objects.get(user_id=user)
        comp.firstname = request.POST["fname"]
        comp.lastname = request.POST['lname']
        comp.state = request.POST['state']
        comp.city = request.POST['city']
        comp.contact = request.POST['phone']
        comp.address = request.POST['address']
        comp.companyname = request.POST['companyname']
        comp.logopic = request.FILES['pp']
        comp.save()
    url = f"/profiledata/{pk}"
    return redirect(url)

def canJobListPage(request):
    alljob = JobDetails.objects.all()
    return render(request,"app/job-list.html",{"alljob":alljob})

def canJobApplyPage(request,pk):
    user = request.session['id']
    can = Candidate.objects.get(user_id=user)
    return render(request,"app/applyjob.html",{"can":can,"job":pk})

def canJobApply(request):
    if request.method == "POST":
        user = request.session["id"]
        job = JobDetails.objects.get(pk=request.POST["pk"])
        # print(job)
        can = Candidate.objects.get(user_id=user)
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        contact = request.POST["phone"]
        state = request.POST["state"]
        city = request.POST["city"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        website = request.POST["website"]
        min_salary = request.POST["minsalary"]
        max_salary = request.POST["maxsalary"]
        experience = request.POST["experience"]
        education = request.POST["education"]
        newapply = ApplyJob.objects.create(job_id=job,can_id=can,firstname=firstname,lastname=lastname,contact=contact,state=state,city=city,email=email,gender=gender,website=website,min_salary=min_salary,max_salary=max_salary,experience=experience,education=education)
        return render(request,"app/job-list.html",{"msg":"Job applied successfully."})

def logout(request):
    request.session.flush()
    return redirect('indexPage')


# ============================== company ============================= #
def compLogout(request):
    del request.session['email']
    del request.session['password']
    return redirect('compIndex')

def compIndexPage(request):
    return render(request,"app/company/index.html")

def postJobPage(request):
    return render(request,"app/company/postjob.html")

def postJob(request,pk):
    if request.method == "POST":
        user = UserMaster.objects.get(pk=pk)
        comp = Company.objects.get(user_id=user)
        jobname = request.POST["jobname"]
        compname = request.POST["compname"]
        compadd = request.POST["compadd"]
        jobdesc = request.POST["jobdesc"]
        qualification = request.POST["qualification"]
        responsibility = request.POST["responsibility"]
        location = request.POST["location"]
        website = request.POST["website"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        salary = request.POST["salary"]
        experience = request.POST["experiance"]
        newjob = JobDetails.objects.create(comp_id=comp,jobname=jobname,companyname=compname,companyaddress=compadd,jobdesc=jobdesc,qualification=qualification,responsibility=responsibility,location=location,email=email,website=website,contact=contact,salary=salary,experience=experience)
        msg = "post added successfully."
        newurl = f"/jobPostListPage/{pk}"
        return redirect(newurl)
        
    
# job post lists page
def jobPostListPage(request,pk):
    comp = Company.objects.get(user_id=pk)
    alljob = JobDetails.objects.all()
    a = []
    for index,i in enumerate(alljob) :
        a.append(ApplyJob.objects.filter(job_id=i).count())
    print(a)        
    return render(request,"app/company/jobpostlist.html",{"alljob":alljob,"comp":comp,"apply":a})

def appliedJobPage(request):
    user = request.session['id']
    comp = Company.objects.get(user_id=user)
    applyjob = ApplyJob.objects.all()
    return render(request,"app/company/applylist.html",{"applyjob":applyjob,"comp":comp})


def adminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"app/admin/index.html")
    else:
        return redirect("adminLoginPage")

def adminLoginPage(request):
    return render(request,"app/admin/login.html")

def adminLogin(request):
    username = request.POST["un"]
    password = request.POST["pp"]
    if username=="admin" and password =="admin":
        request.session.flush()
        request.session["username"] = username
        request.session["password"] = password
        return redirect("adminIndexPage")
    else:
        return render(request,"app/admin/login.html",{"msg":"Username or password incorrect!!!"})
    
def adminCanList(request):
    if 'username' in request.session and 'password' in request.session:
        allcan = UserMaster.objects.filter(role="Candidate")
        return render(request,"app/admin/user.html",{"can":allcan})
    else:
        return redirect("adminLoginPage")

def adminCompList(request):
    if 'username' in request.session and 'password' in request.session:
        allcomp =  UserMaster.objects.filter(role="Company")
        return render(request,"app/admin/user.html",{"comp":allcomp})
    else:
        return redirect("adminLoginPage")