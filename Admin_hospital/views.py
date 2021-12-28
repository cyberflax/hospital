import uuid
from django.contrib import messages as msg
from django.shortcuts import render,redirect
from doctors.models import *
from patient.models import *
from homepage.models import *
from pharmacy.models import *
from .models import *

#for login
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def adminhome(request):
    if request.user.is_authenticated:
        res = {}
        res['dct'] = Dr.objects.all()
        res['pnt'] = patient_record.objects.all()
        res['apmnt'] = appoinmentlist.objects.all()
        return render(request, 'Admin_hospital/adminhome.html', res)

    else:
        
        return redirect('error404')
   

def addblog(request):

    if request.user.is_authenticated:
        res = {}
        res['dr'] = Dr.objects.all()
        res['cat'] = blog_categeory.objects.all()
        res['sub'] = blog_subcategory.objects.all()
        if request.method=='POST':
            title=request.POST['title']
            img = request.FILES['img']
            doc = request.POST['doc']
            desc=request.POST['about']
            cate = request.POST['cat']
            subcate = request.POST['subcat']
            dr=Dr.objects.get(name=doc)
            blog=dr_blogs(title=title,img=img,desc=desc,ctgry=cate,subcate=subcate,doc=dr)
            blog.save()
            msg.success(request,'Blog Added Successfully.')
            return redirect('blog')
        return render(request, 'Admin_hospital/add-blog.html',res)

    else:
        return redirect('error404')
    

def appointmentlist(request):

    if request.user.is_authenticated:
        res = {}
        res['apmnt'] = appoinmentlist.objects.all()
        return render(request, 'Admin_hospital/appointment-list.html', res)

    else:
        return redirect('error404')
   
def blogcategeory(request):
    
    if request.user.is_authenticated:

        ctgry = blog_subcategory.objects.all()
        # product = pharmacy.objects.filter(user=request.user.userType.id)
        if request.method == 'POST': # for edit
            if request.POST.get('catid') is not None:
                # cat = request.POST['catname']
                subcat=request.POST['subname']
                cats= blog_subcategory.objects.get(id=request.POST.get('subid'))
                cats.subcat = subcat
                cats.save()
                msg.success(request,' Blog-category edit successfully')
            elif request.POST.get('cat') is not None:  # for add
                cat = request.POST['cat']
                subcat = request.POST['subcat']
                cats = blog_categeory.objects.values('cat')
                data = {data['cat'].lower() for data in cats}
                subcats = blog_subcategory.objects.values('subcat')
                datas = {data['subcat'].lower() for data in subcats}
                if cat.lower() not in data:
                    spe = blog_categeory(cat=cat)
                    spe.save()
                    cat = blog_subcategory(subcat=subcat, cats=(blog_categeory.objects.get(cat=cat)))
                    cat.save()
                    msg.success(request,'Category Added.')
                    return redirect(request.get_full_path())
                elif subcat.lower() not in datas:
                    cats=blog_categeory.objects.get(cat=cat)
                    cat=blog_subcategory(subcat=subcat,cats=cats)
                    cat.save()
                    msg.success(request,'Sub-Category Added.')
                    return redirect(request.get_full_path())
                else:
                    msg.warning(request, 'Category is already in list')
            elif request.POST.get('catids') is not None:
              # for delete
                products = blog_subcategory.objects.filter(id=request.POST.get('catids'))
                products.delete()
                msg.success(request,'Category Deleted.')
    
        return render(request,'Admin_hospital/blog-category.html',{'cat':ctgry})
    else:
        return redirect('error404')
def blogdetails(request):

    if request.user.is_authenticated:
        Bid=request.GET.get('Bid')
        blog=dr_blogs.objects.get(id=Bid)
        doctor=Dr.objects.get(id=blog.doc.id)
        if request.method == "POST":
            name = request.POST['name']
            review = request.POST['review']
            var = reView( name=name, review=review, dics=doctor, YES=0, NO=0, rating=0)
            var.save()
            msg.success(request,'Review Posted.')
            return redirect(request.get_full_path())
        return render(request, 'Admin_hospital/blog-details.html',{'blog':blog})

    else:
        return redirect('error404')
   

def bloggrid(request):

    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/blog-grid.html')

    else:
        return redirect('error404')
    

def blog(request):

    if request.user.is_authenticated:
        res = {}
        res['blg'] = dr_blogs.objects.all()
        return render(request, 'Admin_hospital/blog.html', res)

    else:
        return redirect('error404')
    

def components(request):
    if request.user.is_authenticated:
         return render(request, 'Admin_hospital/components.html')

    else:
     return redirect('error404')
   

def datatables(request):
    if request.user.is_authenticated:
         return render(request, 'Admin_hospital/data-tables.html')

    else:
        return redirect('error404')
   

def doctorlist(request):

    if request.user.is_authenticated:
        res = {}
        res['dct'] = Dr.objects.all()
        return render(request, 'Admin_hospital/doctor-list.html', res)

    else:
        return redirect('error404')
    

def editblog(request):

    if request.user.is_authenticated:
        res={}
        editdr = Dr.objects.all()
        edit=request.GET.get('edit')
        blog=dr_blogs.objects.get(id=edit)
        
        if request.method=='POST':
            title = request.POST['title']
            img = request.FILES['img']
            doc = request.POST['doc']
            desc = request.POST['about']
            cate = request.POST['cat']
            subcate = request.POST['subcat']
            dr = Dr.objects.get(name=doc)
            # blog = dr_blogs.objects.get(id=edit)
            blog.title=title
            blog.img=img
            blog.desc=desc
            blog.ctgry=cate
            blog.subcate=subcate
            blog.doc=dr
            blog.save()
            msg.success(request,'Blog Edit successfully.')
            return redirect('blog')
        res={'editdr':editdr,'blog':blog}
        return render(request, 'Admin_hospital/edit-blog.html',res)

    else:
        return redirect('error404')
   

def error404(request):
    return render(request, 'Admin_hospital/error-404.html')


def error500(request):
    return render(request, 'Admin_hospital/error-500.html')


def forgotpassword(request):
    return render(request, 'Admin_hospital/forgot-password.html')


def formbasicinput(request):
    if request.user.is_authenticated:
         return render(request, 'Admin_hospital/form-basic-inputs.html')

    else:
     return redirect('error404')
   

def formhorizontal(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/form-horizontal.html')

    else:
        return redirect('error404')
    

def forminputgroups(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/form-input-groups.html')

    else:
      return redirect('error404')
    

def formmask(request):
    if request.user.is_authenticated:
       return render(request, 'Admin_hospital/form-mask.html')

    else:
        return redirect('error404')
    

def formvalidation(request):
    if request.user.is_authenticated:
       return render(request, 'Admin_hospital/form-validation.html')

    else:
        return redirect('error404')
    

def formvertical(request):
    if request.user.is_authenticated:
         return render(request, 'Admin_hospital/form-vertical.html')

    else:
        return redirect('error404')
   

def invoicereport(request):
    if request.user.is_authenticated:

        res = {}
        res['trs'] = appoinmentlist.objects.all()
        res['bill']=billings.objects.all()
         # for delete
        if request.method=='POST':
            if len(request.POST.get('aptid')) != 0:
                ids = request.POST.get('aptid') 
                apt = appoinmentlist.objects.get(id=ids)
                check=checkout.objects.filter(patient=apt.patient,dr_name=apt.doctor,
                time2=apt.time2,date=apt.date,time1=apt.time1)
                if len(check) != 0:
                    check.delete()
                apt.delete()
                msg.success(request,'Invoice Deleted.')
                return redirect(request.get_full_path())
            elif len(request.POST.get('bid')) != 0:
                bills = request.POST.get('bid')
                bill = billings.objects.filter(id=bills)
                bill.delete()
                msg.success(request,'Invoice Deleted successfully.')
                return redirect(request.get_full_path())
                # return redirect(request.META.get('HTTP_REFERER'))
        return render(request, 'Admin_hospital/invoice-report.html', res)

    else:
         return redirect('error404')
   

def lockscreen(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/lock-screen.html')

    else:
        return redirect('error404')
    

def patientlist(request):
    if request.user.is_authenticated:

        res = {}
        res['pnt'] = patient_record.objects.all()
        return render(request, 'Admin_hospital/patient-list.html', res)

    else:
        return redirect('error404')
    

def pharmacylist(request):
    if request.user.is_authenticated:

        phrmcy =pharmacy.objects.all()
        if request.method=='POST':
            if request.POST.get('name') is not None: #for add
                name=request.POST['name']
                phone = request.POST['phone']
                add = request.POST['add']
                img = request.POST['img']
                # phar=pharmacy(name=name,address=add,img=img,contact=phone,opentime="12:00",clostime="12:02")
                # phar.save()  # this not working bcz user is not available
                return redirect(request.get_full_path())
            elif  request.POST.get('phar') is not None:  #for edit
                pharm = request.POST['phrmcy']
                address = request.POST['address']
                img = request.POST['img']
                phone = request.POST['phone']
                phar = pharmacy.objects.get(id=request.POST.get('phar') )
                phar.name=pharm
                phar.img=img
                phar.address=address
                phar.contact=phone
                phar.save()
                msg.success(request,'pharmacy edit successfully.')
                return redirect(request.get_full_path())
            elif request.POST.get('pharids') is not None:  # for delete
                phar = pharmacy.objects.get(id=request.POST.get('pharids'))
                user=User.objects.get(email=phar.email)
                user.delete()
                msg.success(request,'pharmacy delete.')                
                return redirect(request.get_full_path())
        return render(request, 'Admin_hospital/pharmacy-list.html', {'pharma':phrmcy})

    else:
        return redirect('error404')
    

def productlist(request):
    if request.user.is_authenticated:

        prodct=pha_product.objects.all()
        phrmcy=pharmacy.objects.all()
        if request.method=='POST':
            if request.POST.get('pharma') is not None: #for add
                prod = request.POST['prod']
                price = request.POST['price']
                img = request.POST['img']
                phar=pharmacy.objects.get(id=request.POST['pharma'])
                product=pha_product(doc=phar,name=prod,price=price,img=img,expiry_date='1888-11-1')
                product.save()
                msg.success(request,'Product added.')
                return redirect(request.get_full_path())
            elif  request.POST.get('prodid') is not None:  #for edit
                prod = request.POST['name']
                price = request.POST['price']
                img = request.POST['img']
                phar = pha_product.objects.get(id=request.POST['prodid'] )
                phar.name=prod
                phar.img=img
                phar.price=price
                phar.save()
                msg.success(request,'Product Edit successfully.')
                return redirect(request.get_full_path())
            elif request.POST.get('pid') is not None:  # for delete
                phar = pha_product.objects.get(id=request.POST['pid'])
                phar.delete()
                msg.success(request,'Product deleted.')
                return redirect(request.get_full_path())
        return render(request, 'Admin_hospital/product-list.html',{"prod":prodct,'pharma':phrmcy})
    else:
        return redirect('error404')
    

def loginpage(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/admin_login.html')

    else:
        return redirect('error404')
    
def adminprofile(request):
    if request.user.is_authenticated:

        pro=User.objects.get(id=request.user.id)
        profile=hospital_admin_record.objects.filter(user=pro)
        if request.method == 'POST':  # for personal edit

            if request.POST.get('profileid') is not None:
                id1 = request.POST['profileid']
                fname = request.POST['fname']
                lname = request.POST['lname']
                add = request.POST['address']
                city = request.POST['city']
                email = request.POST['email']
                state = request.POST['state']
                dob = request.POST['dob']
                mobile = request.POST['mobile']
                zip = request.POST['zipcode']
                country = request.POST['country']
                user = User.objects.get(id=request.user.id)
                user.first_name = fname
                user.last_name = lname
                user.save()
                profiles = hospital_admin_record.objects.get(id=id1)
                profiles.address = add
                profiles.city = city
                profiles.state = state
                profiles.country = country
                profiles.dob = dob
                profiles.mobile = mobile
                profiles.email = email
                profiles.zipcode = zip
                profiles.save()
                msg.success(request,'Profile Updated.')
                return redirect(request.get_full_path())
            elif request.POST.get('adminid') is not None:
                id = request.POST['adminid']  # admin edit
                name = request.POST['name']
                about = request.POST['about']
                img = request.POST['img']
                profs = hospital_admin_record.objects.filter(id=id)
                if len(profs) > 0:
                    prof = profs[0]
                    prof.about = about
                    prof.name = name
                    prof.img = img
                    prof.save()
                    msg.success(request,'Profile edited success.')
                    return redirect(request.get_full_path())
        
        return render(request, 'Admin_hospital/adminprofile.html',{'profile':profile})
    else:
        return redirect('error404')
def admin_pwd_chng(request):
    if request.user.is_authenticated:
        next=request.GET.get('next')
        if request.method=='POST':
            old = request.POST['oldpwd']
            new = request.POST['newpwd']
            user = User.objects.get(id=request.user.id)
            mail=user.email
            check=user.check_password(old)
            if check==True:
                user.set_password(new)
                user.save()
                user=User.objects.get(email=mail)
                login(request)
                msg.success(request, "password updated")
            else:
                msg.error(request, "incorrect old password")

        return redirect('adminhome')
    else:
        return redirect('error500')
def register(request):
    
    if request.user.is_authenticated!=True:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            confirm=request.POST['confrm']
            usermail = User.objects.filter(email=email)
            usernam=User.objects.filter(username=name)
            # print(name,name.lower(),usernam)
            if len(usermail) !=1 :
                if len(usernam)!=1:
                    user =User.objects.create_superuser(username=name, email=email, password=password)
                    user.save()
                    users=hospital_admin_record(user=user,email=email,name=name)
                    users.save()
                    typeuser = userType(user=user, type='4')
                    typeuser.save()
                    token=str(uuid.uuid4())
                    frgpwd=frgt_pwd(user=user,frg_token=token)
                    frgpwd.save()
                    msg.success(request, "Your account has been successfully created")
                    return redirect('home')
                else: 
                    msg.error(request, "Username is already register.")
            else:
                msg.error(request, "Email is already register.")

        return render(request, 'Admin_hospital/register.html')
    else:
        return redirect('error500')
        
def doc_reviews(request):
    if request.user.is_authenticated:
        res = {}
        res['rvw'] = reView.objects.all()

        dr = request.GET.get('Did')  # for delete
        rev = request.POST.get('rvw')
        review = reView.objects.filter(id=rev)
       
        review.delete()
        # msg.success(request,'Review deleted.')
        return render(request, 'Admin_hospital/doc_reviews.html', res)

    else:
         return redirect('error404')
    

def adminsettings(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/settings.html')

    else:
        return redirect('error404')
    

def specialities(request):
    if request.user.is_authenticated:

        special = speciality.objects.all()
        # product = pharmacy.objects.filter(user=request.user.userType.id)
        if request.method == 'POST': # for edit
            if request.POST.get('speid') is not None:
                name = request.POST['spename']
                # img=request.POST['imgs']
                products = speciality.objects.get(id=request.POST['speid'])
                products.spec = name
                # products.img=img
                products.save()
                msg.success(request, 'speciality edit successfully.')
                return redirect(request.get_full_path())
            elif request.POST.get('spesname') is not None:  # for add
                name = request.POST['spesname']
                img = request.POST['img']
                spes = speciality.objects.values('spec')
                data = {data['spec'].lower() for data in spes}
                if name.lower() not in data:
                    spe = speciality(spec=name,img=img)
                    spe.save()
                    msg.success(request, 'speciality added.')
                    return redirect(request.get_full_path())
                else:
                    msg.error(request, 'speciality is already in list')
                    return redirect(request.get_full_path())
            elif request.POST.get('speids') is not None:
                prod = request.POST['speids']  # for delete
                products = speciality.objects.filter(id=prod)
                products.delete()
                msg.success(request, 'speciality deleted.')
                return redirect(request.get_full_path())
        return render(request, 'Admin_hospital/specialities.html',{'product':special})

    else:
        return redirect('error404')
    

def tablebasic(request):
    if request.user.is_authenticated:
       return render(request, 'Admin_hospital/tables-basic.html')

    else:
        return redirect('error404')
    

def transactionslist(request):
    if request.user.is_authenticated:

        res = {}
        res['bill']=billings.objects.all()
        res['trs'] = appoinmentlist.objects.all()
         # for delete
        if request.method=='POST':
            if len(request.POST.get('tid')) != 0:
                trans = request.POST.get('tid')
                tran = appoinmentlist.objects.get(id=trans)
                check=checkout.objects.filter(patient=tran.patient,dr_name=tran.doctor,
                time2=tran.time2,date=tran.date,time1=tran.time1)
                if len(check) != 0:
                    check.delete()
                tran.delete()
                msg.success(request,'transaction deleted')
                
                return redirect(request.get_full_path())
            elif len(request.POST.get('bid')) != 0:
                bills = request.POST.get('bid')
                bill = billings.objects.filter(id=bills)
                bill.delete()
                msg.success(request,'transaction deleted')
                return redirect(request.get_full_path())
                # return redirect(request.META.get('HTTP_REFERER'))
        return render(request, 'Admin_hospital/transactions-list.html', res)

    else:
        return redirect('error404')
    

def blankpage(request):
    if request.user.is_authenticated:
        return render(request, 'Admin_hospital/Blank-Pages.html')

    else:
        return redirect('error404')
   

