# Generated by Django 3.2.7 on 2021-12-25 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_frgt_pwd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dr',
            name='specialization',
        ),
    ]
