# Generated by Django 3.2.7 on 2021-12-12 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20211212_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dr_blogs',
            old_name='subctgry',
            new_name='subcate',
        ),
        migrations.AlterField(
            model_name='dr_blogs',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
