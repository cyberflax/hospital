from django.shortcuts import render,redirect,HttpResponse
from pharmacy.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import authenticate,login,logout


# Create your views here.



def index(request):
    if request.user.is_authenticated:
            list=[]
            docs=pharmacy.objects.get(id=request.user.pharmacy.id)
            product=pha_product.objects.filter(doc=docs)
            supp=supplier.objects.filter(user=docs)
            user=pharmacy_prod_order.objects.filter(pharmacys=docs)
            for i in user:
                if [i.username,i.phone,i.address,i.email] not in list:
                    list.append([i.username,i.phone,i.address,i.email])
                    # list.append(User.objects.filter(email=i.email))
            dics={'product':list,'date':date.today(),'supp':len(supp),'prod':len(product)}
            return render(request,'home.html',dics)
    
    else:
        return redirect('error404')
def categories(request):
    
    if request.user.is_authenticated:
        product=category.objects.all()
        # product = pharmacy.objects.filter(user=request.user.userType.id)
        if request.method == 'POST':  # for edit
            if request.POST.get('catid') is not None:
                name = request.POST['catname']
                products = category.objects.get(id=request.POST['catid'])
                products.cate = name
                products.save()
                messages.success(request,'Category edit succesfully.')
                return redirect(request.get_full_path())
            elif request.POST.get('catename') is not None:#for add
                name = request.POST['catename']
                cate=category.objects.values('cate')
                data={data['cate'].lower() for data in cate}
                if name.lower() not in data:
                    cat=category(cate=name)
                    cat.save()
                    messages.success(request,'Category added succesfully.')
                    return redirect(request.get_full_path())
                else:
                    messages.warning(request,'category is already in list')

        prod = request.GET.get('catids')#for delete
        products = category.objects.filter(id=prod)
        products.delete()
        # messages.success(request,'Category deleted.')
        # return redirect(request.get_full_path())

        return render(request,'categories.html',{'product':product})
        
    else:
        return redirect('error404')
def sales(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        product = pharmacy_prod_order.objects.filter(pharmacys=pharmcy)

        prod = request.GET.get('product')  # for delete
        pro = pharmacy_prod_order.objects.filter(id=prod)
        pro.delete()

        ids = request.GET.get('productid')         #for edit
        pro = pharmacy_prod_order.objects.filter(id=ids)
        invoice_no=request.GET.get('invoice')
        if len(pro)>0:
            os=pro[0]
            os.invoice=invoice_no
            os.save()
            messages.success(request,'Sale edit succesfully.')
            return redirect(request.get_full_path())
        return render(request,'sales.html',{'product':product})
    
    else:
        return redirect('error404')
def transaction(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        product = pharmacy_prod_order.objects.filter(pharmacys=pharmcy)
        ids = request.GET.get('orderid')  # for delete
        order = pharmacy_prod_order.objects.filter(id=ids)
        if len(order) > 0:
            ob = order[0]
            ob.delete()
            messages.success(request,'Transaction deleted.')
            return redirect(request.get_full_path())

        return render(request,'transactions-list.html',{'product':product})
    else:
        return redirect('error404')
def profile(request):
    
    if request.user.is_authenticated:
        ids = request.GET.get('id')
        pro=User.objects.get(id=request.user.id)
        profile=pharmacy_admin_record.objects.filter(user=pro)

        if request.method=='POST': #for personal edit
            id1 = request.POST.get('profileid')
            if id1 is not None:
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
                user=User.objects.get(id=request.user.id)
                user.first_name = fname
                user.last_name = lname
                user.save()
                profiles = pharmacy_admin_record.objects.get(id=id1)
                profiles.address=add
                profiles.city=city
                profiles.state=state
                profiles.country=country
                profiles.dob=dob
                profiles.mobile = mobile
                profiles.email=email
                profiles.zipcode=zip
                profiles.save()
                messages.success(request,'Profile Updated.')
                return redirect(request.get_full_path())
            elif request.POST.get('adminid') is not None:
                id = request.POST['adminid']  # admin edit
                name = request.POST['name']
                about = request.POST['about']
                img = request.POST['img']
                profs = pharmacy_admin_record.objects.filter(id=id)
                if len(profs) > 0:
                    prof = profs[0]
                    prof.about = about
                    prof.name = name
                    prof.img = img
                    prof.save()             
                    messages.success(request,'Profile update succesfully.')
                    return redirect(request.get_full_path())

        return render(request,'profile.html',{'profile':profile})
        
    else:
        return redirect('error404')
def pwd_chng(request):
    
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
                login(request,user)
                messages.error(request, "password updated")
            else:
                messages.error(request, "incorrect old password")
        return redirect(next)
        
    else:
        return redirect('error404')
def settings(request):
    
    if request.user.is_authenticated:
        if request.method=='POST':
            webname=request.POST['webname']
            weblogo=request.POST['weblogo']
            favicon=request.POST['favicon']
            sett=pharmacy.objects.get(id=request.user.pharmacy.id)
            setts=setting.objects.filter(pharmacy=sett)
            if len(setts)>0:
                prod=setts[0]
                prod.pharmacy=sett
                prod.weblogo=weblogo
                prod.webname=webname
                prod.favicon=favicon
                prod.save()
                messages.success(request,'setting edit succesfully.')
                return redirect(request.get_full_path())
            else:
                prods=setting(webname=webname,weblogo=weblogo,favican=favicon,pharmacy=sett)
                prods.save()
                messages.success(request,'Setting Updated.')
                return redirect(request.get_full_path())
        return render(request,'settings.html')
    
    else:
        return redirect('error404')
def products(request):
    
    if request.user.is_authenticated:
        # phar=request.GET.get('phar_id')
        li=pharmacy.objects.get(id=request.user.pharmacy.id)
        products = pha_product.objects.filter(doc=li)
        products1 = pha_product.objects.filter(id=request.GET.get('prod'))
        products1.delete()
        # messages.success(request,'product deleted.')
        if request.method=='POST': # for edit
                pro=request.POST['phar_ids']
                name = request.POST['prodname']
                cate = request.POST['category']
                price = request.POST['price']
                dis = request.POST['discount']
                gen = request.POST['gen_name']
                product1 = pha_product.objects.get(id=pro)
                product1.price=price
                product1.name=name
                product1.categorie=cate
                product1.discount = dis
                product1.genatic_name=gen
                product1.save()
                messages.success(request,'Product edit succesfully.')
                return redirect(request.get_full_path())
        res= {'product':products,'today':date.today(),'cates':category.objects.all()}
        return render(request,'products.html',res)
    
    else:
        return redirect('error404')
def add_product(request):
    
    if request.user.is_authenticated:
        cates=category.objects.all()
        phars = request.GET.get('phar_id')
        product2 = pharmacy.objects.get(id=request.user.pharmacy.id)
        if request.method=='POST' :
            name=request.POST['prod_name']
            cate = request.POST['category']
            Price = request.POST['Price']
            quantity = request.POST['quantity']
            date = request.POST['ex_date']
            about = request.POST['about']
            images = request.FILES['img']
            prod_name = pha_product.objects.values('name').filter(doc=product2)
            list = {data['name'].lower() for data in prod_name}
            if name.lower() not in list:
                product=pha_product(doc=product2,name=name,img=images,about=about,
                                    price=Price,categorie=cate,quntity=quantity,expiry_date= date )
                product.save()
                messages.success(request, " Product Added Successfully")
            return redirect('products')
        return render(request,'add-product.html',{'cates':cates})
        
    else:
        return redirect('error404')
def outstock(request):
    
    if request.user.is_authenticated:
        li = pharmacy.objects.filter(id=request.user.pharmacy.id)
        # phars = request.GET.get('phar')
        product2 = pharmacy.objects.get(id=request.user.pharmacy.id)
        products = pha_product.objects.filter(id=request.GET.get('prod') , doc=product2)#for delete
        products.delete()
        # messages.success(request,'Product deleted.')

        if request.method == 'POST':  # for edit
            phars = request.POST['phar_ids']
            name = request.POST['gen_name']
            qunt = request.POST['quntity']
            products = pha_product.objects.filter(id=phars)
            if len(products) > 0:
                prod = products[0]
                prod.quntity = qunt
                prod.genatic_name = name
                prod.save()
                messages.success(request,'Product edit succesfully.')
                return redirect(request.get_full_path())
        return render(request,'outstock.html',{'list':li})
    
    else:
        return redirect('error404')
def purchase(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        product = Purchase.objects.filter(pharmacys=pharmcy)
        supp=supplier.objects.filter(user=pharmcy)
        sup=request.GET.get('suppid')
        product1 = Purchase.objects.filter(id=sup)
        product1.delete()
        # messages.success(request,'Purchase deleted.')
            
        if request.method=='POST':
            supp1=request.POST['prod']
            suppl=request.POST['supp']
            prods = Purchase.objects.filter(id=supp1)
            supple=supplier.objects.get(name=suppl)
            if len(prods)>0:
                prod=prods[0]
                prod.supplir=supple
                prod.save()
                messages.success(request,'Purchase edit succesfully.')
                return redirect(request.get_full_path())
        return render(request,'purchase.html',{'product':product,'supp':supp})
    
    else:
        return redirect('error404')
def add_purchase(request):
    
    if request.user.is_authenticated:
        supp=supplier.objects.all()
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        if request.method=='POST':
            medname = request.POST['med_name']
            qun = request.POST['qunt']
            price = request.POST['price']
            img = request.FILES['img']
            cate = request.POST['cate']
            exdate = request.POST['exdate']
            # su_name=request.POST['supp']
            # suppl=supplier.objects.get(name=su_name)
            product = Purchase.objects.values('med_name')
            data = {data['med_name'].lower() for data in product}
            if medname.lower() not in data:
                prod=Purchase(pharmacys=pharmcy,med_name=medname,price=price,
                quntity=qun,img=img,category=cate,ex_date=exdate)
                prod.save()
                messages.success(request,'Purchase add succesfully.')
                return redirect('purchase')
        return render(request,'add-purchase.html',{'supp':supp})
        
    else:
        return redirect('error404')
def order(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        product = pharmacy_prod_order.objects.filter(pharmacys=pharmcy)
        sup = request.GET.get('suppid')
        product1 = pharmacy_prod_order.objects.filter(id=sup,pharmacys=pharmcy)
        product1.delete()
        # messages.success(request,'Order deleted.')
                

        return render(request,'order.html',{'product':product})
    
    else:
        return redirect('error404')
def expired(request):
    
    if request.user.is_authenticated:
        cont= date.today()
        li=pharmacy.objects.filter(id=request.user.pharmacy.id)
        prod = pha_product.objects.filter(id=request.GET.get('ex_ids'))  # for delete
        prod.delete()

        if request.method=='POST':
                ids=request.POST['exid']
                exp = request.POST['expiry']
                gen = request.POST['gentic']
                prod=pha_product.objects.filter(id=ids)
                if len(prod)>0:
                    prods=prod[0]
                    prods.expiry_date=exp
                    prods.genatic_name=gen
                    prods.save()
                    messages.success(request,'Product edit succesfully.')
                    return redirect(request.get_full_path())
        return render(request,'expired.html',{'li':li,'date':cont})
    
    else:
        return redirect('error404')
def suppliers(request):
    
    if request.user.is_authenticated:
        prods=pharmacy.objects.get(id=request.user.pharmacy.id)
        supply = supplier.objects.filter(user=prods)
        prod=pha_product.objects.filter(doc=request.user.pharmacy.id)# editing  options
        supplierid = request.GET.get('suppid')#for delete
        supp=supplier.objects.filter(id=supplierid)
        supp.delete()
        if request.method=='POST':#for edit
            supp = request.POST['supply']
            com = request.POST['company']
            names = request.POST['prod_name']
            supplier1=supplier.objects.filter(id=supp)
            product=pha_product.objects.get(name=names)
            if len(supplier1)>0:
                pro=supplier1[0]
                pro.company=com
                pro.product=product
                pro.save()
                messages.success(request,'Supplier edit succesfully.')
                return redirect(request.get_full_path())
        return render(request,'supplier.html',{'supply':supply,'prod':prod})
    
    else:
        return redirect('error404')
def add_supplier(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        if request.method=='POST':
            img = request.FILES['img[]']
            add = request.POST['address']
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            company = request.POST['company']
            prod_name = supplier.objects.values('email').filter(user=pharmcy)
            list = {data['email'].lower() for data in prod_name}
            if email.lower() not in list:
                supp=supplier(user=pharmcy,name=name,img=img,email=email,mobile=mobile,
                company=company,address=add)
                supp.save()
                messages.success(request,'Supplier add succesfully.')
                return redirect('supplier')
        return render(request,'add-supplier.html')
    
    else:
        return redirect('error404')
def invoice_report(request):
    
    if request.user.is_authenticated:
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        product = pharmacy_prod_order.objects.filter(pharmacys=pharmcy)
        ids = request.GET.get('oderids') #for delete
        order = pharmacy_prod_order.objects.filter(id=ids)
        order.delete()
        order_id=request.GET.get('orderid')  # for edit details
        order=pharmacy_prod_order.objects.filter(id=order_id)
        invoice = request.GET.get('In_no')
        status = request.GET.get('status')
        if len(order)>0:
            ob=order[0]
            ob.invoice=invoice
            ob.payment_status=status
            ob.save()
            messages.success(request,'Invoice edit succesfully.')
            return redirect(request.get_full_path())
        return render(request,'invoice-report.html',{'product':product})
    
    else:
        return redirect('error404')
def invoice_views(request):
    
    if request.user.is_authenticated:
        invoices=request.GET.get('invoice_no')
        all=0
        subtotal=0
        pharmcy=pharmacy.objects.get(id=request.user.pharmacy.id)
        prod=pharmacy_prod_order.objects.filter(id=invoices,pharmacys=pharmcy)
        for i in prod:
            all = (i.total- (i.total * (i.product_id.discount / 100)))
            subtotal=i.quntitys*i.price
        return render(request,'invoice-views.html',{'prod':prod,'all':int(all),'subtotal':subtotal})
    
    else:
        return redirect('error404')