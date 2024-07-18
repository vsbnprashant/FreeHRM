# Generated by Django 4.2.11 on 2024-05-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0004_alter_employeefile_pension_fund_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefile',
            name='paye_income_tax_enabled',
            field=models.BooleanField(default=True, verbose_name='Contributes PAYE'),
        ),
    ]