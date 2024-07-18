from django import forms
from django.forms import Form, FileField

from .models import PayrollGroup, WorkingCalendar, Department, CompanyContact, CompanyBankAccount, PaymentElement, \
    CompanySettings, CompanyPayrollSettings, CompanyTimesheets


class PayrollGroupForm(forms.ModelForm):
    class Meta:
        model = PayrollGroup
        fields = "__all__"



class WorkingCalendarForm(forms.ModelForm):
    class Meta:
        model = WorkingCalendar
        fields = "__all__"

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

class CompanyContactForm(forms.ModelForm):
    class Meta:
        model = CompanyContact
        fields = "__all__"

class UploadForm(Form):
    upload_file = FileField()

class CompanyBankAccountForm(forms.ModelForm):
    class Meta:
        model = CompanyBankAccount
        fields = "__all__"


class PaymentElementForm(forms.ModelForm):
    class Meta:
        model = PaymentElement
        fields = "__all__"

class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = '__all__'  # You can also specify the fields individually if not all should be included.


class CompanyPayrollSettingsForm(forms.ModelForm):
    class Meta:
        model = CompanyPayrollSettings
        fields = '__all__'  # You can also specify the fields individually if not all should be included.


class CompanyTimesheetsForm(forms.ModelForm):
    class Meta:
        model = CompanyTimesheets
        fields = '__all__'  # You can also specify the fields individually if not all should be included.