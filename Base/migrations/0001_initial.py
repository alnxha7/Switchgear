# Generated by Django 4.2.6 on 2024-04-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_code', models.CharField(max_length=50)),
                ('project_name', models.CharField(max_length=255)),
                ('consultant', models.CharField(max_length=255)),
                ('client_name', models.CharField(max_length=255)),
                ('client_number', models.CharField(max_length=20)),
                ('client_email', models.EmailField(max_length=254)),
                ('upload_loadschedule', models.FileField(upload_to='pdfs/')),
                ('upload_sld', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
