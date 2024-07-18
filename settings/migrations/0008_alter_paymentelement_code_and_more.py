# Generated by Django 4.2.11 on 2024-04-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0007_rename_companybank_companybankaccount_paymentelement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentelement',
            name='code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='paymentelement',
            unique_together={('code', 'version')},
        ),
    ]