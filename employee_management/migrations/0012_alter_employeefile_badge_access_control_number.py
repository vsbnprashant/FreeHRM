# Generated by Django 4.2.11 on 2024-05-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0011_remove_employeefile_employment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefile',
            name='badge_access_control_number',
            field=models.CharField(blank=True, default='', max_length=25, verbose_name='Badge Access Control Number'),
        ),
    ]
