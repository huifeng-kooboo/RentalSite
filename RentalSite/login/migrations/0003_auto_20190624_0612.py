# Generated by Django 2.2.1 on 2019-06-23 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_landloadinfo_rental_info_renthouseinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rental_Info',
            new_name='RentalInfo',
        ),
    ]