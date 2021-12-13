from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(speciality)

admin.site.register(hospital_admin_record)

admin.site.register(blog_subcategory)
admin.site.register(blog_categeory)