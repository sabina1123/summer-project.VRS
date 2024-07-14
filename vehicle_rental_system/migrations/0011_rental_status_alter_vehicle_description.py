# Generated by Django 4.2.13 on 2024-06-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental_system', '0010_rental_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Confirm', 'Confirm'), ('Expired', 'Expired')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
