# Generated by Django 4.2.11 on 2024-05-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0012_alter_workingcalendar_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
