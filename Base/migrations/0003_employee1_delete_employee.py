# Generated by Django 5.0 on 2024-06-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_filenew_location_multiproduct_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empcode', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=400)),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
                ('uname', models.CharField(max_length=200)),
                ('passwrd', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
