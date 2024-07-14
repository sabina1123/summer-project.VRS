# Generated by Django 4.2.13 on 2024-06-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental_system', '0007_rename_address_customer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='PaymentMethod',
            field=models.CharField(choices=[('esewa', 'eSewa'), ('cash', 'Cash')], max_length=10),
        ),
    ]
