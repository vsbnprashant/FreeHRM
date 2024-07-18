from django.db import models
import datetime
from common.choices import ContributionCode, EmploymentType
from settings.models import Department, WorkingCalendar, PayrollGroup


# Create your models here.
class Location(models.Model):
    location = models.CharField(max_length=128)
    cost_center = models.CharField(max_length=128, blank=True, default='')
    status = models.CharField(max_length=128, blank=True, default='')
    country = models.CharField(max_length=128, blank=True, default='')
    city = models.CharField(max_length=128, blank=True, default='')
    person_in_charge = models.CharField(max_length=128,  blank=True, default='')

    def __str__(self):
        return f"{self.location} {self.country}"


class EmployeeFile(models.Model):
    is_draft = models.BooleanField(default=True)
    last_name = models.CharField(max_length=40, verbose_name='Surname or Last Name')
    first_name = models.CharField(max_length=40, verbose_name='First Name')
    other_names = models.CharField(max_length=100, blank=True, default='', verbose_name='Other names')
    maiden_name = models.CharField(max_length=50, blank=True, default='', verbose_name='Maiden name')
    nic = models.CharField(max_length=20, verbose_name='National Identity Card Number or Social Security Number', blank=True, default='')
    gender = models.CharField(max_length=5, verbose_name='Gender', blank=True, default='')
    employee_code = models.CharField(max_length=6, verbose_name='Employee Code', blank=True, default='')
    badge_access_control_number = models.CharField(max_length=25, blank=True, default='',
                                                   verbose_name='Badge Access Control Number')
    mobile_number = models.CharField(max_length=15, blank=True, default='', verbose_name='Mobile Number')
    phone = models.CharField(max_length=15, blank=True, default='', verbose_name='Phone Number')
    postcode = models.IntegerField(blank=True, null=True, verbose_name='Post Code')
    date_joined = models.DateField(verbose_name='Joining Date', blank=True, null=True)
    in_current_position_since = models.DateField(verbose_name='In current position since', blank=True, null=True)
    post = models.CharField(max_length=50, verbose_name='Post', blank=True, default='')
    employment_type = models.CharField(
        max_length=6,
        choices=[(tag.code, tag.description) for tag in EmploymentType],
        default=EmploymentType.FULL_TIME.code,
        help_text="Defines the type of employment contract.",
        verbose_name='Employment Type'
    )
    calendar = models.ForeignKey(WorkingCalendar, null=True, on_delete=models.SET_NULL, verbose_name='Calendar', blank=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, verbose_name='Department', blank=True)
    office_site = models.CharField(max_length=20, blank=True, default='', verbose_name='Office Site')
    departure_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Departure Date', null=True, blank=True)
    reason_of_departure = models.CharField(max_length=255, blank=True, default='', verbose_name='Reason of Departure')
    suspension_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Suspension Date', null=True, blank=True)
    reason_for_suspension = models.CharField(max_length=255, blank=True, default='', verbose_name='Reason for Suspension')
    monday_working = models.BooleanField(default=True, verbose_name='Monday', blank=True)
    tuesday_working = models.BooleanField(default=True, verbose_name='Tuesday', blank=True)
    wednesday_working = models.BooleanField(default=True, verbose_name='Wednesday', blank=True)
    thursday_working = models.BooleanField(default=True, verbose_name='Thursday', blank=True)
    friday_working = models.BooleanField(default=True, verbose_name='Friday', blank=True)
    saturday_working = models.BooleanField(default=False, verbose_name='Saturday', blank=True)
    sunday_working = models.BooleanField(default=False, verbose_name='Sunday', blank=True)
    monday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Monday', blank=True)
    tuesday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Tuesday', blank=True)
    wednesday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Wednesday', blank=True)
    thursday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Thursday', blank=True)
    friday_overtime = models.BooleanField(default=True, verbose_name='Overtime permitted on Friday', blank=True)
    saturday_overtime = models.BooleanField(default=False, verbose_name='Overtime permitted on Saturday', blank=True)
    sunday_overtime = models.BooleanField(default=False, verbose_name='Overtime permitted on Sunday', blank=True)

    active_employee = models.BooleanField(default=True, verbose_name='Active Employee', blank=True)
    salary_payment_interval = models.CharField(max_length=30, verbose_name='Salary Payment', blank=True)
    paye_income_tax_enabled = models.BooleanField(default=True, verbose_name='Contributes PAYE', blank=True)
    tan = models.CharField(max_length=32, verbose_name='Tax Acc/Identification Number', blank=True)
    pension_fund_number = models.CharField(max_length=32, verbose_name='Pension Fund Number', blank=True)
    npf_nsf_contribution_enabled = models.BooleanField(default=True, blank=True)
    contribution_code = models.CharField(
        max_length=1,
        choices=[(tag.code, tag.description) for tag in ContributionCode],
        default=ContributionCode.STANDARD.code,
        help_text="Select the type of contribution code.",
        verbose_name='Contribution Code'
    )
    paid_by_bank_transfer = models.BooleanField(default=True, blank=True)
    version = models.IntegerField(default=1)
    origin = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='First Version of this Employee Record')

    def create_new_version(self):
        new_version = self.__class__.objects.get(id=self.id)
        new_version.id = None  # Create a new record
        new_version.version += 1
        new_version.save()

        # Copy related EmployeeBank records
        for bank in self.employeebank_set.all():
            bank.id = None
            bank.employeeFile = new_version
            bank.save()

        # Copy related EmployeeLeaveBalance records
        for leave in self.employeeleavebalance_set.all():
            leave.id = None
            leave.employeeFile = new_version
            leave.save()

        # Copy related EmployeeLoan records
        for loan in self.employeeloan_set.all():
            loan.id = None
            loan.employeeFile = new_version
            loan.save()

        # Copy related EmployeePayrollGroup records
        for payrollgroup in self.employeepayrollgroup_set.all():
            payrollgroup.id = None
            payrollgroup.employeeFile = new_version
            payrollgroup.save()

        return new_version

    def __str__(self):
        return f"#{self.employee_code} - {self.last_name} {self.first_name}"

class EmployeeBank(models.Model):
    employeeFile = models.ForeignKey(EmployeeFile, null=False, on_delete=models.CASCADE)
    bank_code = models.CharField(max_length=128)
    account_number = models.CharField(max_length=128, verbose_name='Bank Account Number')
    currency = models.CharField(max_length=32, verbose_name='Currency')
    split_type = models.CharField(max_length=30, verbose_name='Split Type', blank=True, null=True, default='')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Amount Destined')


class EmployeeEDFDetails(models.Model):
    employeeFile = models.OneToOneField(EmployeeFile,null=False, on_delete=models.CASCADE)
    edf_income_threshold = models.CharField(max_length=30)
    deductions_child_pursuing_undergraduate = models.DecimalField(max_digits=8, decimal_places=2)
    deductions_secured_housing_loan = models.DecimalField(max_digits=8, decimal_places=2)
    deductions_medical_health = models.DecimalField(max_digits=8, decimal_places=2)
    deductions_solar_energy_investment = models.DecimalField(max_digits=8, decimal_places=2)
    deductions_household_employees = models.DecimalField(max_digits=8, decimal_places=2)
    deductions_rainwater_harvesting = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount_exemption = models.DecimalField(max_digits=8, decimal_places=2)
    paye_paid_in_previous_employment = models.BooleanField(default=True)


class EmployeeLeaveBalance(models.Model):
    employeeFile = models.ForeignKey(EmployeeFile, null=False, on_delete=models.CASCADE)
    leave_code = models.CharField(max_length=25)
    amount = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='Allowed')
    rollover = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='Rollover')
    taken = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='Taken')
    available = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='Available')


class EmployeeLoan(models.Model):
    employee_loan_code = models.CharField(max_length=15)
    employeeFile = models.ForeignKey(EmployeeFile, null=False, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    loan_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    paid_month = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Paid Month', null=True, blank=True)
    repayment_monthly_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    repayment_start_month = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Repayment Start Month', null=True, blank=True)
    loan_amount_manually_cleared = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class EmployeePayrollGroup(models.Model):
    employeeFile = models.ForeignKey(EmployeeFile, null=False, on_delete=models.CASCADE)
    payrollGroup = models.ForeignKey(PayrollGroup, null=False, on_delete=models.CASCADE)