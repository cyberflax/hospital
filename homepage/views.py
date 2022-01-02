from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import dr_blogs,Newsletter_subscriber
from doctors.models import Dr, frgt_pwd,reView
from patient.models import favourite, patient_record
from django.contrib import messages
from Admin_hospital.models import speciality
#for send email
from django.core.mail import send_mail
#for html to email
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
def pwd_frgot(request):
    if request.user.is_authenticated!=True:
        if request.method=='POST':
            email=request.POST['email']
            useremail=User.objects.get(email=email)
            frgtoken=frgt_pwd.objects.get(user=useremail)
            ftoken=frgtoken.frg_token
            emails=useremail.email
            mail_msg=f'Hello,Your reset password link is http://127.0.0.1:8000/Pforgot/{ftoken}'
            send_mail('For reset password', mail_msg,settings.EMAIL_HOST_USER, [emails],fail_silently=False)
            messages.success(request, "mail send successfully. check your email. ")
            return redirect('pwd_reset')

        return render(request,'forgot-password.html')
    else:
        return redirect('error500')
def Pforgot(request,id):
    
    if request.user.is_authenticated!=True:
        if request.method=='POST':
            pass1=request.POST['pass1']
            confirm=request.POST['pass2']
            frgpwd=frgt_pwd.objects.get(frg_token=id)
            user=User.objects.get(username=frgpwd)
            print(frgpwd,user,'////////////')
            user.set_password(pass1)
            user.save()
            messages.success(request, "Password change successfully. ")
            return redirect('dlogin')
        
        return render(request,'for_pwd/pwd_reset_confirm.html')
    else:
        return redirect('error500')
def home(request):
    profile = Dr.objects.all()
    blog=dr_blogs.objects.all()
    speciality = speciality.objects.values('spec')
    speciality = {data['spec'] for data in speciality}
    name = request.GET.get('special')
    if name is None:
        names=specility.objects.get(spec=name)
        profile1 = Dr.objects.filter(specialization=names)

        res=profile1
    else:
        res=profile

    re = {'title': profile,'blog':blog,'specialty':speciality,'special':res}
    if request.method=="POST":
        email = request.POST['email1']
        var = Newsletter_subscriber(suscriber_email=email)
        var.save()
        messages.success(request, " Thank You For Your Subscription")
        return redirect('home')
    return render(request,'index.html',re)
def blog_details(request):
    bid = request.GET.get('@//@/')
    Did = request.GET.get('Did')
    doctor=Dr.objects.get(id=Did)

    patient = patient_record.objects.values('name')
    patients = {data['name'] for data in patient}
    if request.method == "POST":
        name = request.POST['name']
        review = request.POST['review']
        patient1 = patient_record.objects.get(name=name)
        if name in patients:
            var = reView(patient=patient1, name=name, review=review, dics=doctor, YES=0, NO=0, rating=0)
            var.save()
            messages.success(request,'Review posted.')
            return redirect(request.get_full_path())
        else:
            messages.success(request, "Your are not patient")
    blogss = dr_blogs.objects.all()
    review = reView.objects.filter(dics=doctor)
    blogs = dr_blogs.objects.get(id=bid)

    rev={'tit':blogs,'alls':blogss,'review':review}
    return render(request,'blog-details.html',rev)
def blog_grid(request):
    blog = dr_blogs.objects.all()
    # blogs = dr_blogs.objects.get(id=bid)
    rev = {'title': blog}
    return render(request,'blog-grid.html',rev)
def blog_list(request):
    blog= dr_blogs.objects.all()
    # blogs = dr_blogs.objects.get(id=bid)
    rev = {'title': blog}
    return render(request,'blog-list.html',rev)

def term_con(request):
    return render(request,'term-condition.html')

def privacy(request):
    return render(request,'privacy-policy.html')

