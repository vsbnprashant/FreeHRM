# Generated by Django 4.2.11 on 2024-05-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0014_remove_companypayrollsettings_salary_calculations_fornightly_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybankaccount',
            name='bank_name',
            field=models.CharField(choices=[('MCBLMUMU', 'Mauritius Commercial Bank'), ('STCBMUMU', 'State Bank of Mauritius'), ('AFBLMUMU', 'AfrAsia Bank'), ('BKONMUMU', 'Bank One'), ('MUAUMUMU', 'MauBank'), ('BMMMUMU', 'Banque des Mascareignes'), ('BARCMUMU', 'ABSA Bank Mauritius')], default='MCBLMUMU', max_length=50),
        ),
        migrations.AlterField(
            model_name='companybankaccount',
            name='currency',
            field=models.CharField(choices=[('MUR', 'MUR'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('JPY', 'JPY')], default='MUR', max_length=32),
        ),
    ]
