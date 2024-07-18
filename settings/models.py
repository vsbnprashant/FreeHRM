import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from common.choices import BankSwiftCodes, SupportedCurrencies


# Create your models here.

class PayrollGroup(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=255,  blank=True, default='')

    def __str__(self):
        return self.name




class WorkingCalendar(models.Model):
    name = models.CharField(unique=True, max_length=64, verbose_name='Name')
    # Monday
    monday_working = models.BooleanField(default=True, verbose_name='Monday Working')
    monday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                         verbose_name='Monday Start Time')
    monday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                       verbose_name='Monday End Time')
    monday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Monday')
    # Tuesday
    tuesday_working = models.BooleanField(default=True, verbose_name='Tuesday Working')
    tuesday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                          verbose_name='Tuesday Start Time')
    tuesday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                        verbose_name='Tuesday End Time')
    tuesday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Tuesday')
    # Wednesday
    wednesday_working = models.BooleanField(default=True, verbose_name='Wednesday Working')
    wednesday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                      verbose_name='Wednesday Start Time')
    wednesday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                    verbose_name='Wednesday End Time')
    wednesday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Wednesday')
    # Thursday
    thursday_working = models.BooleanField(default=True, verbose_name='Thursday Working')
    thursday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                        verbose_name='Thursday Start Time')
    thursday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                      verbose_name='Thursday End Time')
    thursday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Thursday')
    # Friday
    friday_working = models.BooleanField(default=True, verbose_name='Friday Working')
    friday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                      verbose_name='Friday Start Time')
    friday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                    verbose_name='Friday End Time')
    friday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Friday')
    # Saturday
    saturday_working = models.BooleanField(default=False, verbose_name='Saturday Working')
    saturday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                      verbose_name='Saturday Start Time')
    saturday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                    verbose_name='Saturday End Time')
    saturday_overtime = models.BooleanField(default=False, verbose_name='Overtime permitted on Saturday')
    # Sunday
    sunday_working = models.BooleanField(default=False, verbose_name='Sunday Working')
    sunday_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                      verbose_name='Sunday Start Time')
    sunday_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                    verbose_name='Sunday End Time')
    sunday_overtime = models.BooleanField(default=False, verbose_name='Overtime permitted on Sunday')

    lateness_minimum_minutes = models.PositiveSmallIntegerField(default=5, verbose_name='Minimum lateness for Deduction eligibility')

    overtime_minimum_minutes = models.PositiveSmallIntegerField(default=30, verbose_name='Minimum overtime minutes for payment')
    overtime_deduct_lateness = models.BooleanField(default=False, verbose_name='Deduct lateness from overtime?')
    overtime_minimum_arrival_minutes = models.PositiveSmallIntegerField(default=0, verbose_name='Minimum duration to arrive before working hours to count as overtime ')
    overtime_after_hours_break = models.PositiveSmallIntegerField(default=0, verbose_name='Duration to remove from overtime hours for break')
    overtime_after_mins = models.PositiveSmallIntegerField(default=0, verbose_name='After how much time in minutes, does the overtime')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(unique=True, max_length=64)
    description = models.CharField(max_length=255, blank=True, default='')
    parent_department = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Parent Department')
    def get_children(self):
        return Department.objects.filter(parent_department=self)
    def __str__(self):
        return self.name

### Company settings

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def load_without_saving(cls):
        try:
            # Try to load the existing singleton instance
            return cls.objects.get()
        except ObjectDoesNotExist:
            # If it doesn't exist, create a new instance without saving
            return cls()  # This creates a new instance but doesn't save it to the DB


class CompanySettings(SingletonModel):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=128, verbose_name='Short Name')
    tan = models.CharField(max_length=32, verbose_name='TAN number')
    npf = models.CharField(max_length=32, verbose_name='NPF number')
    brn = models.CharField(max_length=32, verbose_name='Business Registration Number')
    nature_of_business = models.CharField(max_length=32)
    incorporation_date = models.DateField(auto_now=False, auto_now_add=False,verbose_name='Incorporation Date')
    def __str__(self):
        return "Company Settings"


class CompanyContact(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=128)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    phone = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    distance_range = models.PositiveSmallIntegerField(default=50, null=True, blank=True)
    primary = models.BooleanField(default=False, verbose_name='Is Primary Contact?')

class CompanyPayrollSettings(SingletonModel):
    period_closing_day_of_month = models.PositiveSmallIntegerField(default=22)
    period_pay_day = models.PositiveSmallIntegerField(default=26)
    declarations_type = models.CharField(max_length=128)
    payslip_template = models.CharField(max_length=128)
    payslip_printing_language = models.CharField(max_length=128)
    salary_calculations_period = models.CharField(max_length=30, default='monthly')
    eoy_bonus = models.CharField(max_length=128)

class CompanyBankAccount(models.Model):
    bank_name = models.CharField(max_length=50, choices=BankSwiftCodes.choices(), default=BankSwiftCodes.MCB.value[0])
    branch = models.CharField(max_length=128)
    account_number = models.CharField(max_length=128)
    iban = models.CharField(max_length=128)
    code = models.CharField(max_length=32)
    currency = models.CharField(max_length=32, choices=SupportedCurrencies.choices(), default=SupportedCurrencies.TYPE1.value[0])
    default_bank = models.BooleanField(default=False, verbose_name='Default Bank?')



class CompanyTimesheets(SingletonModel):
    allow_time_input_from_employee = models.BooleanField(default=True)
    automatic_lateness = models.BooleanField(default=True)
    lateness_field = models.CharField(max_length=32)
    lateness_calculation_type = models.CharField(max_length=32)
    lateness_absence_field = models.CharField(max_length=32)
    automatic_overtime = models.BooleanField(default=True)
    overtime_field = models.CharField(max_length=32)
    overtime_calculation_type = models.CharField(max_length=32)
    overtime_calculation_option = models.CharField(max_length=32)


class PaymentElement(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    formula = models.TextField()  # Stores the Excel-like formula
    order = models.IntegerField()  # The order in which this element should be processed
    version = models.IntegerField(default=1)
    origin = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
                                          verbose_name='First Version of this Payment Element')

    def calculate(self, context):
        # This method will use the formula and context to calculate the value
        # You will need to implement the logic to parse and execute the formula
        pass

    class Meta:
        ordering = ['order']  # Ensures elements are ordered properly by default
        unique_together = ('code', 'version',)

    def __str__(self):
        return self.title