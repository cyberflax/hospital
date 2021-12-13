from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import dr_blogs,Newsletter_subscriber
from doctors.models import Dr,reView
from patient.models import patient_record
from django.contrib import messages
# Create your views here.

def home(request):
     profile = Dr.objects.all()
     blog=dr_blogs.objects.all()
     speciality = Dr.objects.values('specialization')
     speciality = {data['specialization'] for data in speciality}
     name = request.GET.get('special')
     profile1 = Dr.objects.filter(specialization=name)
     if name is None:
         res=profile
     else:
         res=profile1

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
        print( 'ratttttttt', name, review, patient1)
        if name in patients:
            var = reView(patient=patient1, name=name, review=review, dics=doctor, YES=0, NO=0, rating=0)
            var.save()
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

