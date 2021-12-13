# Generated by Django 3.2.7 on 2021-12-12 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Admin_hospital', '0002_speciality_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='hospital_admin_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('img', models.ImageField(upload_to='')),
                ('dob', models.DateField(blank=True, null=True)),
                ('mobile', models.IntegerField(null=True)),
                ('about', models.TextField()),
                ('zipcode', models.IntegerField(null=True)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hos_admin_record', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
