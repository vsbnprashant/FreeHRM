# Generated by Django 4.2.11 on 2024-05-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0022_alter_employeeleavebalance_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefile',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
