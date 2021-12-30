from django.shortcuts import render,redirect
from .models import *
from patient.models import *
from Admin_hospital.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
import uuid
#for login
from django.contrib.auth import authenticate,login,logout

def Doctor_profile(request,id):
    
    # if request.user.is_authenticated:
         # bid= request.GET.get('@//@/')
        profile=Dr.objects.get(id=id)
        patient = patient_record.objects.values('name')
        patients = {data['name'] for data in patient}
        if request.method == "POST":
            if request.POST.get('name') != None:
                name = request.POST['name']
                review = request.POST['review']
                rating = request.POST['rating']
                patient1 = patient_record.objects.get(name=name)
                if name in patients:
                    var = reView(patient=patient1,name=name, review=review,dics=profile,YES=0,NO=0,rating=rating)
                    var.save()
                    messages.success(request,'Review Posted.')
                    return redirect(request.get_full_path())
                else:
                    messages.success(request, "Your are not patient")
            elif request.POST.get('reid') != 0:
                name = request.POST['re_name']
                review = request.POST['reply']
                # rating = request.POST['ratings']
                rv=reView.objects.get(id=request.POST.get('reid'))
                patient1 = patient_record.objects.get(name=name)
                # if name in patients:
                var = rvw_reply(rvw=rv,patient=patient1,name=name, review=review,
                doc=profile,YES=0,NO=0,rating=0)
                var.save()
                messages.success(request,'Reply Posted.')
                return redirect(request.get_full_path())

        review = reView.objects.filter(dics=profile)
        loc=Loca_tions.objects.filter(doc=profile)
        pro=Dr.objects.filter(id=id)
        buss_ho=Buss_Ho.objects.filter(doc1=profile)
        ov_view=Ov_view.objects.filter(doc=profile)
        reply=rvw_reply.objects.filter(doc=profile)
        # if request.user.userType.type == '1' is not None:
        #     pa_names=patient_record.objects.get(id=request.user.patient_record.id)# for favourite checked
        #     favt=favourite.objects.values('dr_name').filter(pa_name=pa_names)
        #     fav=[i['dr_name'] for i in favt]
        # else:
        #     print('')
        res={'title':profile,'review':review,'location':loc,
        'Buss_Ho':buss_ho,'over':ov_view,'reply':reply}
        return render(request,'doctor/doctor-profile.html',res)
    
def Doctor_register(request):
    
    if request.user.is_authenticated != True:
        userlist=Dr.objects.values('email')
        userlis={data['email'].lower() for data in userlist}
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            confirm=request.POST['confirm']
            usermail = User.objects.filter(email=email)
            usernam=User.objects.filter(username=name)
            print(name,name.lower(),usernam)
            if len(usermail) !=1:
                if len(usernam)!=1:
                    user =User.objects.create_user(username=name, email=email, password=password)
                    user.save()
                    user1 = Dr(user=user, name=name, email=email,fees_starting=0,fees_end=0 )
                    user1.save()
                    typeuser = userType(user=user, type='2')
                    typeuser.save()
                    token=str(uuid.uuid4())
                    frgpwd=frgt_pwd(user=user,frg_token=token)
                    frgpwd.save()
                    if user is None:
                        messages.error(request, "invalid user")
                    else:
                        messages.success(request, "Your account has been successfully created")
                    return redirect('home')
                    
                else:
                    messages.error(request, "username is already register.")
            else:
                messages.error(request, "Email is already register.")
        return render(request,'doctor/doctor-register.html')
    else:
        return redirect('error500')
def change_password(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            old = request.POST['oldpwd']
            new = request.POST['newpwd']
            # confirm = request.POST['cnfpwd']
            user = User.objects.get(id=request.user.id)
            mail=user.email
            check=user.check_password(old)
            if check==True:
                user.set_password(new)
                user.save()
                user=User.objects.get(email=mail)
                login(request,user)
                messages.error(request, "password updated")
            else:
                messages.error(request, "incorrect old password")
            return redirect('change_password')
        return render(request,'patient/change-password.html')
    else:
        return redirect('error500')
def dlogin(request):
    
    if request.user.is_authenticated != True:
        if request.method=='POST':
            loginemail = request.POST['email']
            user=User.objects.filter(email=loginemail)
            if len(user)==1 :
                username = User.objects.get(email=loginemail).username
                pass1 = request.POST['password']
                user= authenticate(username=username,password=pass1)
                users=User.objects.get(email=loginemail)
                check=users.check_password(pass1)
                if check==True:
                    # if user is not None:
                            login(request,user)
                            # if not request.user.is_authenticated:
                            #     messages.success(request, 'user none')
                            #     return redirect('dlogin')
                            # else:
                            messages.success(request,F'{username} you are successfully logged In')
                            return redirect('home')
                else:
                    messages.error(request, 'Wrong password')
            else:
                messages.error(request,'Email is not registered')
            return redirect('dlogin')
        return render(request,'login.html')
    else:
        return redirect('error500')
def dlogout(request):
    logout(request)
    messages.success(request,f'{request.user.username} you are successfully logged Out')
    return redirect('home')
def doctor_dashboard(request):
    
    if request.user.is_authenticated:
        
        dr = Dr.objects.get(id=request.user.Dr.id)
        list= checkout.objects.filter(dr_name=dr)
        totalapp=len(list)
        doctors=Dr.objects.get(id=request.user.Dr.id)
        p_list=mypatient.objects.filter(Dr_names=doctors)
        current_date=date.today()
        return render(request,'doctor/doctor-dashboard.html',{'list':list,'now':current_date,'length':totalapp,'pcount':len(p_list)})
    else:
        return redirect('error500')
def doctor_profile_setting(request):
    
    if request.user.is_authenticated:
            userids=request.GET.get('profile')
            doctor=Dr.objects.filter(id=userids)
            profile = Dr.objects.get(id=userids)
            if request.method == "POST":
                        fname = request.POST['fname']
                        lname = request.POST['lname']
                        user = User.objects.get(id=request.user.id)
                        user.first_name = fname
                        user.last_name = lname
                        user.save()
                        img = request.POST['img']
                        qulification = request.POST['qulification']
                        # speciality = request.POST['speciality']
                        fees1 = request.POST['f1']
                        fees2= request.POST['f2']
                        city = request.POST['city']
                        gender = request.POST['gender']
                        if len(doctor)>0:
                            ob = doctor[0]
                            ob.user=user
                            ob.name = request.user.username
                            ob.email = request.user.email
                            ob.img = img
                            ob.qulification= qulification
                            # ob.specialization=speciality
                            ob.address = city
                            ob.fees_starting=fees1
                            ob.fees_end = fees2
                            ob.gender=gender
                            ob.save()
                        about = request.POST['about']
                        user1 = Ov_view(doc=profile, about=about)
                        user1.save()

                        profile1 = Ov_view.objects.get(doc=user1)

                        # services = request.POST['services']
                        # ser=servies_add.objects.get(service=services)
                        # user1 = servi_ses(dr=profile1,servics=ser)
                        # user1.save()

                        #
                        # if len(ser)>0:
                        #     ob=ser[0]
                        #     ob.service=services
                        #     # ob.save()
                        #     print(ob,ob.id,'ooo')
                        #     users1 = servi_ses(dr=profile1)
                        #     users1.servics.add(request.ob.service)
                        #     users1.save()
                        # else:
                        #     print('invalid servise')

                        # specialist = request.POST['specialist']
                        # spec=specifications_add.objects.get(specifications=specialist)
                        # user1 = Specific_ation(dr=profile1,specification=spec)
                        # user1.save()
                        # us = user1.specification.create(specifications=spec)
                        # print(user1,'//specc')

                        aw_name = request.POST['aw_name']
                        year = request.POST['year']
                        field = request.POST['field']
                        awrd=Awards.objects.filter(dr=profile1, aw_name=aw_name,aw_desc=field)
                        if len(awrd)>0:
                            aw=awrd[0]
                            aw.dr = profile1
                            aw.aw_name = aw_name
                            aw.aw_year = year
                            aw.aw_desc = field
                            aw.save()
                        else:
                            user1 = Awards(dr=profile1, aw_name=aw_name,aw_year=year,aw_desc=field)
                            user1.save()

                        institude = request.POST['institude']
                        YOC = request.POST['YOC']
                        YOA = request.POST['YOA']
                        degree = request.POST['degree']
                        edu=Educat_ion.objects.filter(dr=profile1,degree=degree)
                        if len(edu) > 0:
                            ed = edu[0]
                            ed.dr = profile1
                            ed.univercity = institude
                            ed.degree = degree
                            ed.YOP = YOC
                            ed.YOA = YOA
                            ed.save()
                        else:
                            user1 = Educat_ion(dr=profile1, univercity=institude,degree=degree,YOP=YOC,YOA=YOA)
                            user1.save()

                        hosp_name = request.POST['hosp_name']
                        yop = request.POST['yop']
                        yop1 = request.POST['yop1']
                        designation=request.POST['designation']
                        exp=Exp_erince.objects.filter(dr=profile1,exp_filled =hosp_name,experince=designation)
                        if len(exp)>0:
                            ex=exp[0]
                            ex.dr = profile1
                            ex.exp_filled = hosp_name
                            ex.YO_exp_start = yop
                            ex.YO_exp_till = yop1
                            ex.experince = designation
                            ex.save()
                        else:
                            user1 = Exp_erince(dr=profile1,exp_filled =hosp_name,YO_exp_start = yop,YO_exp_till = yop1,experince=designation)
                            user1.save()

                        name = request.POST['cli_name']
                        fee = request.POST['fees']
                        add = request.POST['clinic_add']
                        loc= Loca_tions.objects.filter(doc=profile,clinics_name=name)
                        if len(loc)>0:
                            locs=loc[0]
                            locs.doc = profile
                            locs.clinics_name = name
                            locs.clinic_add = add
                            locs.fees = fee
                            locs.save()
                        else:
                            user1 = Loca_tions(doc=profile,clinics_name=name, clinic_add=add,fees=fee)
                            user1.save()
                # add2 = request.POST['add2']
                # add3 = request.POST['add3']
                # city = request.POST['citys']
                # state = request.POST['state']
                # country = request.POST['country']
                # postalcode = request.POST['postalcode']
                #
                # membership = request.POST['membership']
                # registration = request.POST['registration']
                # # res_year = request.POST['res_year']
                        messages.success(request, 'profile updated ')
                        return redirect(request.get_full_path())
                        # spec=speciality.objects.all()
            res={'spec':specifications_add.objects.all(),
            # 'special':speciality.objects.all(),
            'serv':servies_add.objects.all()}
            return render(request,'doctor/doctor-profile-settings.html',res)
    else:
        return redirect('error500')
    
    
def reviews(request):
    
    if request.user.is_authenticated:
        dr=Dr.objects.get(id=request.user.Dr.id)
        rev=reView.objects.filter(dics=dr)
        return render(request,'doctor/reviews.html',{'review':rev})
    else:
        return redirect('error500')
def like(request):
    
    if request.user.is_authenticated:
        bid=request.GET.get('@//@/')
        next=request.GET.get('next')
        prod_list = reView.objects.filter(id=bid)
        if request.GET.get('@//@/') != None:
            if len(prod_list) > 0:
                ob = prod_list[0]
                if ob.YES >= 0:
                    ob.YES+= 1
                    ob.save()
            return redirect(next)
        elif request.GET.get('re_like') != None:
                prod_list=rvw_reply.objects.filter(id=request.GET.get('re_like'))
                if len(prod_list) > 0:
                    ob = prod_list[0]
                    if ob.YES >= 0:
                        ob.YES+= 1
                        ob.save()
                return redirect(next)
    else:
        return redirect('error500')
def dislike(request):
    
    if request.user.is_authenticated:
        bid=request.GET.get('@//@/')
        next = request.GET.get('next')
        prod_list = reView.objects.filter(id=bid)
        if request.GET.get('@//@/') != None:
            if len(prod_list) > 0:
                ob = prod_list[0]
                if ob.NO >= 0:
                    ob.NO+= 1
                    ob.save()
            return redirect(next)
        elif request.GET.get('re_dislike') != None:
            prod_list=rvw_reply.objects.filter(id=request.GET.get('re_dislike'))
            if len(prod_list) > 0:
                ob = prod_list[0]
                if ob.NO >= 0:
                    ob.NO+= 1
                    ob.save()
            return redirect(next)
    else:
        return redirect('error500')
def appointments(request):

    if request.user.is_authenticated:
        doctor=request.GET.get('doctor')
        dr=Dr.objects.get(id=doctor)
        appoin=checkout.objects.filter(dr_name=dr)
        res={'app':appoin}
        return render(request,'doctor/appointments.html',res)
    else:
        return redirect('error500')
def appo_delete(request):

    if request.user.is_authenticated:
        # app_id = request.GET.get('id')
        checkid=request.GET.get('id')
        next = request.GET.get('next')
        check=checkout.objects.get(id=checkid)
        check.delete()
        messages.success(request,'Appointment deleted.')
        return redirect(next)
    else:
        return redirect('error500')
def schedule(request):
    
    if request.user.is_authenticated:
        path1=request.get_full_path()
        dr = Dr.objects.get(id=request.user.Dr.id)
        path3=request.get_full_path()
        time = for_bookings.objects.filter(name=dr)
        day = for_bookings.objects.values('day')
        days = {datas['day'] for datas in day}
        x = request.GET.get('dayy')
        # x2=book_times.objects.get(dr=x)
        x1 = book_times.objects.filter(dr=x)
        time1 = request.GET.get('timeid')
        day = request.GET.get('dayid')
        p = book_times.objects.filter(id=day)
        # pcun=p.times.all().count()
        for i in p:
            z = i.times.remove(time1)
            if i.times.all().count()==0:
                p.delete()
                messages.success(request,'Schedule Time is deleted.')
            return redirect(request.META.get('HTTP_REFERER'))
        res = {'time': time, 'days': days, 'x': x1}
        return render(request,'doctor/schedule-timings.html',res)
    else:
        return redirect('error500')
def invoices(request):
    
    if request.user.is_authenticated:
        # doctor = request.GET.get('invoice')
        dr = Dr.objects.get(id=request.user.Dr.id)
        invoice = appoinmentlist.objects.filter(doctor=dr)
        bill=billings.objects.filter(doctor=dr)
        if request.GET.get('Oid') is not None:
            oderid = request.GET.get('Oid')
            pat_id = request.GET.get('pid')
            pat=patient_record.objects.get(id=pat_id)
            app = appoinmentlist.objects.get(patient=pat,id=oderid)
            check=checkout.objects.filter(patient=pat,dr_name=dr,time2=app.time2,date=app.date,time1=app.time1)
            if len(check) is not 0:
                check.delete()
            app.delete()
            messages.success(request,'Invoice deleted.')
            return redirect(request.META.get('HTTP_REFERER'))
        elif request.GET.get('aid') is not None:
            aid = request.GET.get('aid')
            pat = request.GET.get('pat')
            pat=patient_record.objects.get(id=pat)
            check = billings.objects.get(patient=pat,id=aid)
            check.delete()
            messages.success(request,'Invoice deleted.')
            return redirect(request.META.get('HTTP_REFERER'))
        res = {'invoice': invoice,'bill':bill}
        return render(request,'doctor/invoices.html',res)
    else:
        return redirect('error500')
def chat_doctor(request):
    
    if request.user.is_authenticated:
        dr = Dr.objects.get(id=request.user.Dr.id)
        chat = checkout.objects.filter(dr_name=dr)
        li=[]
        for i in chat:
            pat=patient_record.objects.get(id=i.patient.id)
            if pat not in li:
               li.append(pat)
        return render(request,'doctor/chat-doctor.html',{'list':li})
    else:
        return redirect('error500')
def checkup(request):
    
    if request.user.is_authenticated:
        patientid = request.GET.get('id')
        patients=patient_record.objects.filter(id=patientid)
        # timing=checkout.objects.filter(id=patientid)
        oid = request.GET.get('Oid')
        patents=patient_record.objects.get(id=patientid)
        tiing=checkout.objects.filter(id=oid,patient=patents)

        tiings=appoinmentlist.objects.filter(id=oid,patient=patents)
        res = {'patient': patients,'time':tiing,'time1':tiings}

        return render(request,'doctor/checkup.html',res)
    else:
        return redirect('error500')
def my_patients(request):
    
    if request.user.is_authenticated:
        doctors=Dr.objects.get(id=request.user.Dr.id)
        patientlist=mypatient.objects.filter(Dr_names=doctors)
        return render(request,'doctor/my-patients.html',{'list':patientlist})
    else:
        return redirect('error500')
def allpatient(request):
    
    if request.user.is_authenticated:
        dr_id=request.GET.get('doctor')
        pa_id = request.GET.get('pa_id')
        doctors=Dr.objects.get(id=dr_id)
        patients=patient_record.objects.get(id=pa_id)
        Oid = request.GET.get('Oid')
        # my_patients = mypatient.objects.filter(Dr_names=doctors, pa_names=patients)
        check = checkout.objects.filter(dr_name=doctors, patient=patients,id=Oid)
        patientid = request.GET.get('pa_id')
        patients = patient_record.objects.filter(id=request.GET.get('pa_id'))
        patient1 = patient_record.objects.get(id=patientid)
        patientss = User.objects.get(username=patient1.name)
        if request.method=='POST':
            age = request.POST['age']
            BG = request.POST['bgroup']
            gender = request.POST['gender']
            dob = request.POST['dob']
            if len(patients) > 0:
                ob = patients[0]
                ob.patient = patientss
                ob.age = age
                ob.gender = gender
                ob.Blood_group = BG
                ob.DOB = dob
                ob.save()
            else:
                patient = patient_record(patient=patientss, age=age, Blood_group=BG, DOB=dob,gender=gender)
                patient.save()
            BP = request.POST['BP']
            BP1 = request.POST['BP1']
            GL = request.POST['GL']
            GL1 = request.POST['GL1']
            BT = request.POST['BT']
            HR = request.POST['HR']
            patient1 = patient_record.objects.get(id=pa_id)
            pat = patient_record.objects.filter(id=request.GET.get('pa_id'))
            dashBord=patient_dashB.objects.filter(patient_name=patient1)
            if len(dashBord) > 0:
                os = dashBord[0]
                os.patient_name = patient1
                os.heart_rate = HR
                os.BP_mg = BP
                os.BP_dl = BP1
                os.body_temp = BT
                os.Glucose_Level_up = GL
                os.Glucose_Level_to = GL1
                os.BMI_Status = 0
                os.Heart_Rate_Status = 0
                os.FBC_Status = 0
                os.Weight_Status = 0
                os.save()
            else:
                patient1 = patient_record.objects.get(id=pa_id)
                patients = patient_dashB(patient_name=patient1, heart_rate=HR, BP_mg=BP, BP_dl=BP1,
                                        body_temp=BT, Glucose_Level_up=GL, Glucose_Level_to=GL1,
                                        BMI_Status=0, Heart_Rate_Status=0, FBC_Status=0, Weight_Status=0)
                patients.save()
            messages.success(request, 'successfully detail updated')
        for data in check:
            pa_id=data.patient
            dr_id=data.dr_name
            my_patients = mypatient.objects.filter(Dr_names=dr_id, pa_names=pa_id)
            # app=appoinmentlist(doctor=dr_id,patient=pa_id,date=data.date,time1=data.time1,time2=data.time2)
            prec=prescriptions(patient=pa_id,date=data.date,doctor=dr_id)
            prec.save()
            # bill=billings(appoinment=app,patient=pa_id,doctor=dr_id,amount=data.amount,paid_on_date=data.date,invoice_no=0)
            # bill.save()
            medical=medical_records(patient=pa_id,desc='',attachment='',date=data.date,doctor=dr_id)
            medical.save()

            if len(my_patients)>0:
                ob=my_patients[0]
                ob.Dr_names=dr_id
                ob.pa_names=pa_id
                ob.save()
            else:
                my_patienT = mypatient(Dr_names=dr_id, pa_names=pa_id)
                my_patienT.save()
            data.delete()
        return redirect('my_patient')
    else:
        return redirect('error500')

def pagenotfound(request):
    return render(request,'notfound.html')


