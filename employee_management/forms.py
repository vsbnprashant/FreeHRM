from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, FileField

from .models import Location, EmployeeFile, EmployeeBank, EmployeeLeaveBalance, EmployeePayrollGroup


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class UploadForm(Form):
    upload_file = FileField()


class EmployeeFileForm(forms.ModelForm):
    finalize_version = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = EmployeeFile
        fields = '__all__'  # Assuming you want to include all fields from the model

    def clean(self):
        cleaned_data = super().clean()
        date_joined = cleaned_data.get('date_joined')
        in_current_position_since = cleaned_data.get('in_current_position_since')
        departure_date = cleaned_data.get('departure_date')
        reason_of_departure = cleaned_data.get('reason_of_departure')
        suspension_date = cleaned_data.get('suspension_date')
        reason_for_suspension = cleaned_data.get('reason_for_suspension')
        employee_code = cleaned_data.get('employee_code')
        version = cleaned_data.get('version')

        # Check if in_current_position_since is valid
        if date_joined and in_current_position_since:
            if in_current_position_since < date_joined:
                self.add_error('in_current_position_since',
                               "In-current-position-since date cannot be before the joining date.")

        # Check if departure_date and reason_of_departure are valid
        if departure_date and not reason_of_departure:
            self.add_error('reason_of_departure', "Reason of departure is required when a departure date is provided.")

        # Check if suspension_date and reason_for_suspension are valid
        if suspension_date and not reason_for_suspension:
            self.add_error('reason_for_suspension',
                           "Reason for suspension is required when a suspension date is provided.")

            # Check for unique employee_code and version combination
        if employee_code and version:
            existing_record = EmployeeFile.objects.filter(employee_code=employee_code, version=version)
            if self.instance.pk:
                existing_record = existing_record.exclude(pk=self.instance.pk)
            if existing_record.exists():
                self.add_error('employee_code',
                               f"Employee code '{employee_code}' with version '{version}' already exists.")

        return cleaned_data


class EmployeeBankForm(forms.ModelForm):
    class Meta:
        model = EmployeeBank
        fields = ['bank_code', 'account_number', 'currency', 'split_type', 'amount']

    def clean(self):
        cleaned_data = super().clean()
        split_type = cleaned_data.get('split_type')
        amount = cleaned_data.get('amount')

        if (split_type and not amount) or (amount and not split_type):
            raise ValidationError('Both "Split Type" and "Amount" must be provided together.')

        return cleaned_data


class EmployeeLeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeaveBalance
        fields = ['leave_code', 'amount', 'rollover', 'taken', 'available']


from django import forms
from .models import EmployeeLoan


class EmployeeLoanForm(forms.ModelForm):
    class Meta:
        model = EmployeeLoan
        fields = ['employee_loan_code', 'loan_amount', 'loan_charges', 'paid_month', 'repayment_monthly_amount',
                  'repayment_start_month', 'loan_amount_manually_cleared']


class EmployeePayrollGroupForm(forms.ModelForm):
    class Meta:
        model = EmployeePayrollGroup
        fields = ['payrollGroup']
