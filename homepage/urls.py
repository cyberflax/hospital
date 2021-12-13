
from django.contrib import admin
from django.urls import path,include
from homepage import views

urlpatterns = [

    path('', views.home, name='home'),
    path('blog-details', views.blog_details, name='blog_details'),
    path('blog-grid', views.blog_grid, name='blog_grid'),
    path('blog-list', views.blog_list, name='blog_list'),
    path('blog-details', views.blog_details, name='blog_details'),
    path('term_con/', views.term_con, name='term_con'),


]