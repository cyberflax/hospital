
from django.contrib import admin
from django.urls import path,include
from Admin_hospital import views

urlpatterns = [

    # path('dashboard/', views.dashboard, name='dashboard'),

    path('admindashboard/', views.adminhome, name='adminhome'),
    path('add-blog/', views.addblog, name='addblog'),
    path('appointment-list/', views.appointmentlist, name='appointmentlist'),
    path('blank-page/', views.blankpage, name='blankpage'),
    path('blog-details/', views.blogdetails, name='blogdetails'),
    path('blog-grid/', views.bloggrid, name='bloggrid'),
    path('blog/', views.blog, name='blog'),
    path('blogcategeory/',views.blogcategeory,name='blogcategeory'),
    path('edit-blog/', views.editblog, name='editblog'),
    path('components/', views.components, name='components'),
    path('data-tables/', views.datatables, name='datatables'),
    path('doctor-list/', views.doctorlist, name='doctorlist'),
    path('error-404/', views.error404, name='error404'),
    path('error-500/', views.error500, name='error500'),
    path('forgot-password/', views.forgotpassword, name='frgt_pwd'),
    path('form-basic-input/', views.formbasicinput, name='formbasicinput'),
    path('form-horizontal/', views.formhorizontal, name='formhorizontal'),
    path('form-input-groups/', views.forminputgroups, name='forminputgroups'),
    path('form-mask/', views.formmask, name='formmask'),
    path('form-validation/', views.formvalidation, name='formvalidation'),
    path('form-vertical/', views.formvertical, name='formvertical'),
    path('invoice-report/', views.invoicereport, name='invoicereport'),
    path('lock-screen/', views.lockscreen, name='lockscreen'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('patient-list/', views.patientlist, name='patientlist'),
    path('pharmacy-list/', views.pharmacylist, name='pharmacylist'),
    path('product-list/', views.productlist, name='productlist'),
    path('adminprofile/', views.adminprofile, name='adminprofile'),
    path('admin_pwd_chng/', views.admin_pwd_chng, name='admin_pwd_chng'),

    path('register/', views.register, name='register'),
    path('doc-reviews/', views.doc_reviews, name='doc_reviews'),
    path('adminsettings/', views.adminsettings, name='adminsettings'),
    path('specialities/', views.specialities, name='specialities'),
    path('table-basic/', views.tablebasic, name='tablebasic'),
    path('transactions-list/', views.transactionslist, name='transactionslist'),
    path('datatables/', views.datatables, name='datatables'),
    path('tablebasic/', views.tablebasic, name='tablebasic'),

]