# Generated by Django 3.2.7 on 2021-12-09 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate', models.CharField(max_length=30)),
                ('date_created', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('img', models.ImageField(upload_to='')),
                ('mobile', models.IntegerField()),
                ('company', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='pharmacy.pha_product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='pharmacy.pharmacy')),
            ],
        ),
        migrations.CreateModel(
            name='setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webname', models.CharField(max_length=30)),
                ('weblogo', models.ImageField(upload_to='')),
                ('favican', models.ImageField(upload_to='')),
                ('pharmacy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='setting', to='pharmacy.pharmacy')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('quntity', models.IntegerField()),
                ('ex_date', models.CharField(max_length=30)),
                ('created_date', models.DateField(auto_now=True)),
                ('img', models.ImageField(upload_to='')),
                ('pharmacys', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy', to='pharmacy.pharmacy')),
                ('supplir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to='Admin_pharmacy.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='pharmacy_admin_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('img', models.ImageField(upload_to='')),
                ('dob', models.DateField()),
                ('mobile', models.IntegerField()),
                ('about', models.TextField()),
                ('zipcode', models.IntegerField()),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_admin_record', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
