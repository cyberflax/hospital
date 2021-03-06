# Generated by Django 3.2.7 on 2021-12-27 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0004_alter_pharmacy_contact'),
        ('Admin_pharmacy', '0005_alter_pharmacy_admin_record_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='pharmacy.pha_product'),
        ),
    ]
