from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(pharmacy_admin_record)

admin.site.register(category)

admin.site.register(supplier)

admin.site.register(Purchase)
admin.site.register(setting)