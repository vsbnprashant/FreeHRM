# Generated by Django 4.2.11 on 2024-05-07 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0005_alter_employeefile_paye_income_tax_enabled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeefile',
            old_name='normal_working_friday',
            new_name='friday_working',
        ),
        migrations.RenameField(
            model_name='employeefile',
            old_name='normal_working_monday',
            new_name='monday_working',
        ),
        migrations.RenameField(
            model_name='employeefile',
            old_name='normal_working_thursday',
            new_name='thursday_working',
        ),
        migrations.RenameField(
            model_name='employeefile',
            old_name='normal_working_tuesday',
            new_name='tuesday_working',
        ),
        migrations.RenameField(
            model_name='employeefile',
            old_name='normal_working_wednesday',
            new_name='wednesday_working',
        ),
        migrations.AddField(
            model_name='employeefile',
            name='friday_overtime',
            field=models.BooleanField(default=True, verbose_name='Overtime permitted on Friday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='monday_overtime',
            field=models.BooleanField(default=True, verbose_name='Overtime permitted on Monday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='saturday_overtime',
            field=models.BooleanField(default=False, verbose_name='Overtime permitted on Saturday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='saturday_working',
            field=models.BooleanField(default=False, verbose_name='Saturday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='sunday_overtime',
            field=models.BooleanField(default=False, verbose_name='Overtime permitted on Sunday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='sunday_working',
            field=models.BooleanField(default=False, verbose_name='Sunday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='thursday_overtime',
            field=models.BooleanField(default=True, verbose_name='Overtime permitted on Thursday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='tuesday_overtime',
            field=models.BooleanField(default=True, verbose_name='Overtime permitted on Tuesday'),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='version',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='employeefile',
            name='wednesday_overtime',
            field=models.BooleanField(default=True, verbose_name='Overtime permitted on Wednesday'),
        ),
        migrations.AlterUniqueTogether(
            name='employeefile',
            unique_together={('employee_code', 'version')},
        ),
        migrations.RemoveField(
            model_name='employeefile',
            name='normal_working_saturday',
        ),
        migrations.RemoveField(
            model_name='employeefile',
            name='normal_working_sunday',
        ),
    ]