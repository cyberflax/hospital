# Generated by Django 3.2.7 on 2021-12-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_billings_appoinment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptions',
            name='prec_name',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
