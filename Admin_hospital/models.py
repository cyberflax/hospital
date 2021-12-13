from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class hospital_admin_record(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='hos_admin_record')
    name=models.CharField(max_length=30)
    email = models.EmailField()
    img=models.ImageField()
    dob = models.DateField(blank=True,null=True)
    mobile = models.IntegerField(null=True)
    about = models.TextField()
    zipcode = models.IntegerField(null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    address=models.TextField()

    def __str__(self):
        return self.name

class speciality(models.Model):
    spec = models.CharField(max_length=30)
    img=models.ImageField(blank=True)
    date_created=models.DateField(auto_now=True)
    def __str__(self):
        return self.spec


# class setting(models.Model):
#     admin=models.OneToOneField(hospital_admin_record,on_delete=models.CASCADE,related_name='setting')
#     webname=models.CharField(max_length=30)
#     weblogo=models.ImageField()
#     favican=models.ImageField()
#
#     def __str__(self):
#         return self.webname

