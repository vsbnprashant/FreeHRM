# Generated by Django 4.2.11 on 2024-05-11 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0007_alter_employeefile_departure_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefile',
            name='post',
            field=models.CharField(max_length=50, verbose_name='Post'),
        ),
    ]
