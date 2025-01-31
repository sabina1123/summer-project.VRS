# Generated by Django 4.2.13 on 2024-06-13 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental_system', '0003_alter_vehicle_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='PaymentMethod',
            field=models.CharField(choices=[('C', 'CASH'), ('O', 'ONLINE')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='RentalRate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
