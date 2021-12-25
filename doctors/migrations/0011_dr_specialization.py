# Generated by Django 3.2.7 on 2021-12-25 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_hospital', '0007_blog_subcategory'),
        ('doctors', '0010_remove_dr_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='dr',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Drs', to='Admin_hospital.speciality', unique=True),
        ),
    ]