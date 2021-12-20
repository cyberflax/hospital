
from django.contrib import messages
from django.shortcuts import render,redirect
from doctors.models import *
from patient.models import *
from homepage.models import *
from pharmacy.models import *
from .models import *


# Create your views here.

def adminhome(request):
    if request.user.is_authenticated:
        res = {}
        res['dct'] = Dr.objects.all()
        res['pnt'] = patient_record.objects.all()
        res['apmnt'] = appoinmentlist.objects.all()
        messages.warning(request,'ppppp')

    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/adminhome.html', res)


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
            return redirect('blog')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/add-blog.html',res)


def appointmentlist(request):

    if request.user.is_authenticated:
        res = {}
        res['apmnt'] = appoinmentlist.objects.all()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/appointment-list.html', res)

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
                    messages.success(request,'Category Added.')
                    return redirect(request.get_full_path())
                elif subcat.lower() not in datas:
                    cats=blog_categeory.objects.get(cat=cat)
                    cat=blog_subcategory(subcat=subcat,cats=cats)
                    cat.save()
                    messages.success(request,'Sub-Category Added.')
                    return redirect(request.get_full_path())
                else:
                    messages.warning(request, 'Category is already in list')
            elif request.POST.get('catids') is not None:
              # for delete
                products = blog_subcategory.objects.filter(id=request.POST.get('catids'))
                products.delete()
    else:
        return redirect('error404')
    return render(request,'Admin_hospital/blog-category.html',{'cat':ctgry})
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
            return redirect(request.get_full_path())
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/blog-details.html',{'blog':blog})


def bloggrid(request):

    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/blog-grid.html')


def blog(request):

    if request.user.is_authenticated:
        res = {}
        res['blg'] = dr_blogs.objects.all()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/blog.html', res)


def components(request):
    if request.user.is_authenticated:
        print('done')
    else:
     return redirect('error404')
    return render(request, 'Admin_hospital/components.html')


def datatables(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/data-tables.html')


def doctorlist(request):

    if request.user.is_authenticated:
        res = {}
        res['dct'] = Dr.objects.all()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/doctor-list.html', res)


def editblog(request):

    if request.user.is_authenticated:
        res={}
        editdr = Dr.objects.all()
        edit=request.GET.get('edit')
        blog=dr_blogs.objects.get(id=edit)
        print(blog,'//')
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
        res={'editdr':editdr,'blog':blog}
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/edit-blog.html',res)


def error404(request):
    return render(request, 'Admin_hospital/error-404.html')


def error500(request):
    return render(request, 'Admin_hospital/error-500.html')


def forgotpassword(request):
    return render(request, 'Admin_hospital/forgot-password.html')


def formbasicinput(request):
    if request.user.is_authenticated:
        print('done')
    else:
     return redirect('error404')
    return render(request, 'Admin_hospital/form-basic-inputs.html')


def formhorizontal(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/form-horizontal.html')


def forminputgroups(request):
    if request.user.is_authenticated:
        print('done')
    else:
      return redirect('error404')
    return render(request, 'Admin_hospital/form-input-groups.html')


def formmask(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/form-mask.html')


def formvalidation(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/form-validation.html')


def formvertical(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/form-vertical.html')


def invoicereport(request):
    if request.user.is_authenticated:

        res = {}
        res['trs'] = appoinmentlist.objects.all()
        ids = request.POST.get('aptid')  # for delete
        apt = appoinmentlist.objects.filter(id=ids)
        apt.delete()
    else:
         return redirect('error404')
    return render(request, 'Admin_hospital/invoice-report.html', res)


def lockscreen(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/lock-screen.html')


def login(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/login.html')


def patientlist(request):
    if request.user.is_authenticated:

        res = {}
        res['pnt'] = patient_record.objects.all()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/patient-list.html', res)


def pharmacylist(request):
    if request.user.is_authenticated:

        phrmcy =pharmacy.objects.all()
        if request.method=='POST':
            if request.POST.get('phone') is not None: #for add
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
                phar = pharmacy.objects.get(id=request.POST.get('phar') )
                phar.name=pharm
                phar.img=img
                phar.address=address
                phar.save()
            elif request.POST.get('pharids') is not None:  # for delete
                phar = pharmacy.objects.get(id=request.POST.get('pharids'))
                phar.delete()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/pharmacy-list.html', {'pharma':phrmcy})


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
            elif request.POST.get('pid') is not None:  # for delete
                phar = pha_product.objects.get(id=request.POST['pid'])
                phar.delete()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/product-list.html',{"prod":prodct,'pharma':phrmcy})


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
                    return redirect(request.get_full_path())
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/adminprofile.html',{'profile':profile})
def admin_pwd_chng(request):
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
            messages.error(request, "password updated")
        else:
            messages.error(request, "incorrect old password")

    return redirect('adminhome')
def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm=request.POST['confrm']
        user =User.objects.create_superuser(username=name, email=email, password=password)
        user.save()
        users=hospital_admin_record(user=user,email=email,name=name)
        users.save()
        typeuser = userType(user=user, type='4')
        typeuser.save()
                # name1 = request.POST['name']
                # email1 = request.POST['email']
                # user1 = Dr(user=user, name=name1, email=email1,fees_starting=0,fees_end=0 )
                # user1.save()
                # typeuser = userType(user=user, type='2')
                # typeuser.save()
                # if user is None:
                #     messages.error(request, "invalid user")
                # else:
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
        # else:
        #     messages.error(request, "Email or name is already register.")

    return render(request, 'Admin_hospital/register.html')
def reviews(request):
    if request.user.is_authenticated:
        res = {}
        res['rvw'] = reView.objects.all()

        dr = request.GET.get('Did')  # for delete
        rev = request.POST.get('rvw')
        review = reView.objects.filter(id=rev)
        print(review,dr,rev,'/xxxx')
        review.delete()
    else:
         return redirect('error404')
    return render(request, 'Admin_hospital/reviews.html', res)


def settings(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/settings.html')


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
            elif request.POST.get('spesname') is not None:  # for add
                name = request.POST['spesname']
                img = request.POST['img']
                spes = speciality.objects.values('spec')
                data = {data['spec'].lower() for data in spes}
                if name.lower() not in data:
                    spe = speciality(spec=name,img=img)
                    spe.save()
                else:
                    messages.arning(request, 'speciality is already in list')

        prod = request.GET.get('speids')  # for delete
        products = speciality.objects.filter(id=prod)
        products.delete()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/specialities.html',{'product':special})


def tablebasic(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/tables-basic.html')


def transactionslist(request):
    if request.user.is_authenticated:

        res = {}
        res['trs'] = appoinmentlist.objects.all()

         # for delete
        trans = request.POST.get('tid')
        tran = appoinmentlist.objects.filter(id=trans)
        tran.delete()
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/transactions-list.html', res)


def blankpage(request):
    if request.user.is_authenticated:
        print('done')
    else:
        return redirect('error404')
    return render(request, 'Admin_hospital/Blank-Pages.html')


