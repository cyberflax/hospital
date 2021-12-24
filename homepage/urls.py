
from django.contrib import admin
from django.urls import path,include
from homepage import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('blog-details', views.blog_details, name='blog_details'),
    path('blog-grid', views.blog_grid, name='blog_grid'),
    path('blog-list', views.blog_list, name='blog_list'),
    path('blog-details', views.blog_details, name='blog_details'),
    path('term_con/', views.term_con, name='term_con'),
    
    # path('password_reset/',
    # auth_views.PasswordResetView.as_view(template_name='forgot-password.html'),
    # name='pwd_reset'),
    path('reset/',views.pwd_frgot,name='pwd_reset'),
    path('Pforgot/<str:id>/',views.Pforgot,name='pforgot')
    # path('password_reset/done/',
    # auth_views.PasswordResetDoneView.as_view(template_name='for_pwd/reset_pwd_sent.html')
    # ,name='pwd_reset_done'),
        
    # path('reset/<uidb64>/<token>/',
    # auth_views.PasswordResetConfirmView.as_view,
    # name='pwd_reset_confirm'),

    # path('reset/done/',
    # auth_views.PasswordResetCompleteView.as_view(template_name='for_pwd/pwd_reset_complete.html'),
    # name='pwd_reset_complete'),


]