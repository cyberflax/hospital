import datetime
from django.shortcuts import render,redirect
from .models import *
import uuid

from Admin_pharmacy.models import pharmacy_admin_record
from doctors.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from patient.models import patient_record

# Create your views here.

def pharmacy_details(request):
    
    if request.user.is_authenticated:
        bid = request.GET.get('@//@/')
        pha= pharmacy.objects.all()
        medical = pharmacy.objects.get(id=bid)
        reviews = pha_review.objects.filter(dics=medical.id)
        patient = patient_record.objects.values('name')
        patients = {data['name'] for data in patient}
        if request.method == "POST":
            name = request.POST['title']
            review = request.POST['review']
            rating = request.POST['rating']
            if name in patients:
                var = pha_review(name=name, review=review,dics=medical,YES=0,NO=0,rating=rating)
                var.save()
                messages.success(request, "Review posted.")
                return redirect(request.get_full_path())
            else:
                messages.error(request, "Your are not patient.please register.")

        res = {'title': medical}

        return render(request,'pharmacy/pharmacy-details.html',res)
    
    else:
        return redirect('error500')
def liked(request):
    
    if request.user.is_authenticated:
        bid=request.GET.get('@//@/')
        next=request.GET.get('next')
        prod_list = pha_review.objects.filter(id=bid)
        if len(prod_list) > 0:
            ob = prod_list[0]
            if ob.YES >= 0:
                ob.YES+= 1
                ob.save()
        return redirect(next)
    else:
        return redirect('error500')
def disliked(request):
    
    if request.user.is_authenticated:
        bid=request.GET.get('@//@/')
        next = request.GET.get('next')
        prod_list = pha_review.objects.filter(id=bid)
        if len(prod_list) > 0:
            ob = prod_list[0]
            if ob.NO >= 0:
                ob.NO+= 1
                ob.save()
        return redirect(next)
    else:
        return redirect('error500')
def pharmacy_search(request):
    
    if request.user.is_authenticated:
        medical=pharmacy.objects.all()
        res={'title':medical}
        return render(request,'pharmacy/pharmacy-search.html',res)
    else:  
        return redirect('error500')
def product_description(request):
    
    if request.user.is_authenticated:
        bdid = request.GET.get('@//@/')
        product1 = pha_product.objects.get(id=bdid)

        res={'title':product1}
        return render(request,'pharmacy/product-description.html',res)
    else:
        return redirect('error500')
def product_all(request):
    
    if request.user.is_authenticated:
        list=[]
        re={}
        total=0
        today=datetime.date.today()
        bdid=request.GET.get('@//@/')# for product description
        if bdid is None:
            list.append(pha_product.objects.all())
            categories1 = pha_product.objects.values('categorie')
            categories = {data['categorie'] for data in categories1}
            re.update({'cat': categories})
            if request.method == 'POST':
                cat_filter = request.POST.getlist('cat1')
                data=''
                list.clear()
                if len(cat_filter) > 0:
                    for i in cat_filter:
                        data = data + i + " "
                        prod_list1 = pha_product.objects.filter(categorie=i)
                        list.append(prod_list1)
            p=pha_product.objects.all().count()
            total+=p
        else:
            product=pharmacy.objects.get(id=bdid)
            prod_list = pha_product.objects.filter(doc=product)
            list.append(prod_list)
            categories1 = pha_product.objects.values('categorie').filter(doc=product)
            categories = {data['categorie'] for data in categories1}
            re.update({'cat':categories})
            if request.method=='POST':
                cat_filter = request.POST.getlist('cat1')
                data = ''
                list.clear()
                if len(cat_filter)>0:
                    for i in cat_filter:
                        data = data + i + " "
                        prod_list1 = pha_product.objects.filter(doc=product,categorie=i)
                        list.append(prod_list1)
            p = pha_product.objects.filter(doc=product).count()
            total += p
        count = 0
        for i in list:
            for j in i:
                if j.expiry_date >= today:
                    count += 1
        lis=[]
        for i in list:
          for j in i:
            li=j.doc.address
            if li not in lis:
                lis.append(li)
        res = {'title':list,'cat':re,'count':count,'total':total,'today':today,'add':lis}

        return render(request,'pharmacy/product-all.html',res)
    else:
        return redirect('error500')
def pharmacy_register(request):
    
    if request.user.is_authenticated  !=True:
        userlist=pharmacy.objects.values('email')
        userlis={data['email'] for data in userlist}
        if request.method == "POST":
                names = request.POST['name']
                emails = request.POST['email']
                passwords = request.POST['password']
                usermail = User.objects.filter(email=emails)
                usernam = User.objects.filter(username=names)

                if len(usermail) !=1 :
                    if len(usernam)!=1:
                        user = User.objects.create_user(username=names, email=emails, password=passwords)
                        user.save()
                        usr = pharmacy_admin_record(user=user)
                        usr.save()
                        typeuser=userType(user=user,type='5')
                        typeuser.save()
                        pharma=pharmacy(email=emails,user=user,name=names)
                        pharma.save()
                        token=str(uuid.uuid4())
                        frgpwd=frgt_pwd(user=user,frg_token=token)
                        frgpwd.save()
                        if user is None:
                            messages.error(request, "invalid user")
                        else:
                            messages.success(request, "Your account has been successfully created")
                        return redirect('home')
                    else:
                        messages.error(request,'username is already register.')
                else:
                    messages.error(request, "Email is already register.")
                    return redirect(request.get_full_path())
        return render(request,'pharmacy/pharmacy-register.html')
    else:
        return redirect('error500')
def medicine_cart(request):
    
    if request.user.is_authenticated:
        itemlist=product_cart.objects.filter(user_id=request.user.id)
        li=[]
        dic={}
        total=0
        # ob=product_cart.objects.all()
        # ob.delete()
        for data in itemlist:
            pharmacy_id=data.pharmacy_name
            prodct_id=data.product_id
            print(prodct_id,';;;;;;',data.id)
            products=pha_product.objects.get(id=prodct_id)
            allprice=products.price*data.quntity
            total+=allprice
            li.append([products,allprice,data.quntity])
            sub=total+25 #shippnig/tax
            all=(sub-(sub*(products.discount/100)))
            dic={'product':li,'total':total,'sub':sub,'alltotal':all,'dis':products.discount}
        return render(request,'pharmacy/cart.html',dic)
    else:
        return redirect('error500')
def add_to_cart(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('@//@/')
        pharmacy_id = request.GET.get('next')
        product = pha_product.objects.get(doc=pharmacy_id,id=product_id)
        cartitem=product_cart.objects.filter(user_id=request.user.id,pharmacy_name=product.doc.name,product_id=product_id)
        if len(cartitem)>0:
            ob = cartitem[0]
            ob.quntity += 1
            ob.save()
        else:
            products=product_cart(user_id=request.user.id,Sku_no=product.doc.id,pharmacy_name=product.doc.name,quntity=1,product_id=product.id)
            products.save()
        # else:
        #     messages.warning(request,'Please Login')
        #     return redirect('dlogin')
        return redirect('medicine_cart')
    else:
        return redirect('error500')    
def minus(request):
    
    if request.user.is_authenticated:
        prodid = request.GET.get('quntity')
        docid = request.GET.get('next')
        itemlist = product_cart.objects.filter(user_id=request.user.id, product_id=prodid,pharmacy_name=docid)
        if len(itemlist) > 0:
            ob = itemlist[0]
            if ob.quntity != 0:
                ob.quntity -= 1
                ob.save()
            else:
                ob.delete()
        return redirect('medicine_cart')
    else:
        return redirect('error500')
def plus(request):
    
    if request.user.is_authenticated:
        prodid = request.GET.get('quntity')
        docid = request.GET.get('next')
        itemlist = product_cart.objects.filter(user_id=request.user.id, product_id=prodid, pharmacy_name=docid)
        if len(itemlist) > 0:
            ob = itemlist[0]
            if ob.quntity != 0:
                ob.quntity += 1
                ob.save()
        return redirect('medicine_cart')
    else:
        return redirect('error500')
def delete(request):
    
    if request.user.is_authenticated:
        prodid = request.GET.get('id')
        docid = request.GET.get('next')
        itemlist = product_cart.objects.filter(user_id=request.user.id, product_id=prodid, pharmacy_name=docid)
        itemlist.delete()
        return redirect('medicine_cart')
    else:
        return redirect('error500')
def payment_success(request):
    
    if request.user.is_authenticated:
        userid = request.GET.get('user')
        return render(request,'pharmacy/payment-success.html')
    else:
        return redirect('error500')
def product_checkout(request):
    
    if request.user.is_authenticated:
        itemlist = product_cart.objects.filter(user_id=request.user.id)
        li=[]
        total=0
        # total=0
        dic={}
        for data in itemlist:
            pharmacy_id = data.pharmacy_name
            prodct_id = data.product_id
            products = pha_product.objects.get(id=prodct_id)
            allprice = products.price * data.quntity
            total += allprice
            if products.quntity < data.quntity:
                messages.error(request, F'{products.name} product is out of stock quntity is  {products.quntity} available')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                li.append([products, allprice, data.quntity])
            sub = total + 25  # shippnig/tax
            all =(sub-(sub * (products.discount / 100)))
            dic = {'product': li, 'total': total,'sub':sub, 'alltotal': int(all),'dis':products.discount}
        return render(request,'pharmacy/product-checkout.html',dic)
    else:
        return redirect('error500')
def product_order(request):
    
    if request.user.is_authenticated:
        itemlist = product_cart.objects.filter(user_id=request.user.id)
        li = []
        total = 0
        
        for data in itemlist:
            pharmacy_name = data.pharmacy_name
            product_id = data.product_id
            products = pha_product.objects.get(id=product_id)
            allprice = products.price * data.quntity
            total+=allprice
            li.append([products, allprice, data.quntity])
            sub = total + 25  # shippnig/tax

            if request.method == "POST":
                contact_no = request.POST['phone']
                address = request.POST['address']
                shipping = request.POST['shipping']
                cardname = request.POST['card_name']
                cardno = request.POST['card_no']
                cvv= request.POST['cvv']
                expyear = request.POST['exp_year']
                expmonth = request.POST['exp_month']
                mail=User.objects.get(email=request.user.email)
                var = pharmacy_prod_order(username=request.user.username,phone=contact_no,address=address,
                                        shipping_details=shipping,card_name=cardname,card_no=cardno,
                                        exp_month=expmonth,exp_year=expyear,cvv=cvv,product_id=products,
                                        pharmacys=products.doc,price=products.price,total=sub,product_name=products.name,
                                        quntitys=data.quntity,invoice=0,email=mail)
                var.save()
                prods = pha_product.objects.filter(id=data.product_id)
                qunt=products.quntity-data.quntity
                if len(prods)>0:
                    ob=prods[0]
                    ob.quntity=qunt
                    ob.save()
                # messages.success(request, 'Order placed successfully ')
            data.delete()
        messages.success(request, 'Order placed successfully ')
        return redirect('payment_success')
    else:
        return redirect('error500')