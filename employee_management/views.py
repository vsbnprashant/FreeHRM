from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from csv import DictReader
from io import TextIOWrapper

from common.choices import GenderOptions, SalaryCalculationsPeriodChoices, ContributionCode, EmploymentType, \
    BankSwiftCodes, SupportedCurrencies, AmountSplitType, LeaveType
from settings.models import Department, WorkingCalendar, PayrollGroup
from .models import Location, EmployeeFile, EmployeeBank, EmployeeLeaveBalance, EmployeeLoan, EmployeePayrollGroup


# Create your views here.

@permission_required("employee_management.view_location")
def locations(request):
    """
    This is a sample function loading the locations table
    """
    mylocations = Location.objects.all().values()
    template = loader.get_template('all_locations.html')
    context = {
        'mylocations': mylocations,
    }

    return HttpResponse(template.render(context, request))


@permission_required("employee_management.view_location")
def details(request, id):
    """
    This is a sample function loading the details of a location
    """
    mylocation = Location.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mylocation': mylocation,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    """
    This function loads the Dashboard for the Employee Management module
    """
    # template = loader.get_template('main.html')
    # return HttpResponse(template.render())
    active_employee_count = EmployeeFile.objects.filter(active_employee=True).count()
    return render(request, 'main.html', {'active_employee_count': active_employee_count})


from .forms import LocationForm, UploadForm, EmployeeFileForm, EmployeeBankForm, EmployeeLeaveBalanceForm, \
    EmployeeLoanForm, EmployeePayrollGroupForm
from django.shortcuts import render, redirect, get_object_or_404


@permission_required("employee_management.view_location")
def location_edit(request, id=None):
    """
    This function is used to edit a location
    The id parameter is optional, if it is provided, the function will edit the location with the given id
    If the id is not provided, it will create a new location
    """
    if id:
        location = get_object_or_404(Location, id=id)
        form = LocationForm(request.POST or None, instance=location)
    else:
        form = LocationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('locations_list')
        else:
            # If the form is not valid, print errors in the console (can be modified based on requirements)
            print(form.errors)

    context = {
        'form': form,
        'location': location if id else Location()
    }
    return render(request, 'edit.html', context)


@permission_required("employee_management.delete_location")
def destroy(request, id):
    """
    This function is used to delete a location
    """
    location = Location.objects.get(id=id)
    location.delete()
    return redirect("locations_list")

class UploadView(PermissionRequiredMixin, View):
        """
        This class is used to upload a CSV file to create multiple locations
        """
        permission_required = ("employee_management.add_location")

        def get(self, request, *args, **kwargs):
            return render(request, "upload.html", {"form": UploadForm()})

        def post(self, request, *args, **kwargs):
          upload_file = request.FILES["upload_file"]
          rows = TextIOWrapper(upload_file, encoding="utf-8", newline="")
          row_count = 0
          form_errors = []
          for row in DictReader(rows):
            row_count +=1
            form = LocationForm(row)
            if not form.is_valid():
               form_errors = form.errors
               break
            form.save()
          return render(request, "upload.html",
                        {
                          "form": UploadForm(),
                          "form_errors": form_errors,
                          "row_count": row_count,
                        })





## EmployeeFile
@permission_required("employee_management.add_employeefile")
def employee_create_new_version(request, id=None):
    """
    This function is used to create a new version of an EmployeeFile
    The id parameter is required, it is the id of the EmployeeFile to create a new version of it
    """
    new_version = None
    if id:
        employeefile = get_object_or_404(EmployeeFile, id=id)

        # check if draft exists
        latest_draft = EmployeeFile.objects.filter(
            origin=employeefile.origin,
            is_draft=True
        ).order_by('-version').first()

        if latest_draft is not None:
            return redirect('employeefile_edit_url', id=latest_draft.id)


        new_version = employeefile.create_new_version()
        new_version.origin = employeefile.origin
        new_version.is_draft = True
        new_version.save()

    return redirect('employeefile_edit_url', id=new_version.id)


@permission_required("employee_management.view_employeefile")
def get_latest_non_draft_version(request, id=None):
    latest_version = None
    if id:
        input_employee_file = get_object_or_404(EmployeeFile, id=id)
        latest_employee_file = EmployeeFile.objects.filter(
            origin=input_employee_file.origin,
            is_draft=False
        ).order_by('-version').first()

    return redirect('employeefile_edit_url', id=latest_employee_file.id)

def is_latest_non_draft_version(input_employee_file=None):
    if input_employee_file:
        latest_employee_file = EmployeeFile.objects.filter(
            origin=input_employee_file.origin,
            is_draft=False
        ).order_by('-version').first()

        if latest_employee_file is None:
            return False

        if input_employee_file.id == latest_employee_file.id:
            return True

    return False


@permission_required("employee_management.view_employeefile")
def employeefile_edit(request, id=None):
    # Define variables that will be used in the template
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    departments = Department.objects.all()
    calendars = WorkingCalendar.objects.all()
    allversions = []
    employeefile = EmployeeFile()
    salarypaymentperiods = [(choice.value[0], choice.value[1]) for choice in SalaryCalculationsPeriodChoices]

    if id:
        employeefile = get_object_or_404(EmployeeFile, id=id)
        form = EmployeeFileForm(request.POST or None, instance=employeefile)
        # Get related objects for the EmployeeFile
        employee_banks = EmployeeBank.objects.filter(employeeFile=employeefile)
        leave_balances = EmployeeLeaveBalance.objects.filter(employeeFile=employeefile)
        loans = EmployeeLoan.objects.filter(employeeFile=employeefile)
        payroll_groups = EmployeePayrollGroup.objects.filter(employeeFile=employeefile)
        allversions = EmployeeFile.objects.filter(employee_code=employeefile.employee_code).order_by('-version')
    else:
        # If no ID is provided, initialize a new form
        form = EmployeeFileForm(request.POST or None)
        # Initialize empty lists for related objects
        employee_banks = []
        leave_balances = []
        loans = []
        payroll_groups = []

    # If the form is submitted
    if request.method == "POST":
        print('Draft')
        print(request.POST.get('is_draft'))
        if (request.POST.get('is_draft') == 'true'):

            try:
                # Start a database transaction
                with transaction.atomic():
                    # Save the form but don't commit to the database yet
                    employeefile = form.save()
                    # Mark the EmployeeFile as a draft
                    employeefile.is_draft = True
                    # Redirect to the list of EmployeeFiles
                    return redirect('employeefile_list_url')
            except (ValidationError, ValueError) as e:
                # If there's an error, print it and render the form again
                print(e)
                return render(request, 'employeefile_edit.html',
                              {'error': e,
                               'form': form,
                               'genders': GenderOptions.choices(),
                               'employeefile': employeefile,
                               'departments': departments,
                               'calendars': calendars,
                               'days': days,
                               'contribution_codes': ContributionCode.choices(),
                               'salarypaymentperiods': salarypaymentperiods,
                               'employmenttypes': EmploymentType.choices(),  # Pass the enum to the template,
                               'employee_banks': employee_banks,
                               'leave_balances': leave_balances,
                               'loans': loans,
                               'payroll_groups': payroll_groups,
                               'is_latest_non_draft_version': is_latest_non_draft_version(employeefile),
                               'draft_eligible': (employeefile.is_draft or employeefile.id != None) and (is_latest_non_draft_version()) # you can create a draft if not already in draft
                               })
            # end of draft


        elif form.is_valid() :
            # Save the form and commit to the database
            f = form.save()
            # Mark the EmployeeFile as not a draft
            f.is_draft = False
            f.save()
            # Redirect to the list of EmployeeFiles
            return redirect('employeefile_list_url')

        else:
            # If the form is not valid, print errors in the console (can be modified based on requirements)
            # Manually update employeefile attributes to submitted data
            for field in form.fields:
                if(field!='finalize_version'):
                  setattr(employeefile, field, form.cleaned_data.get(field, getattr(employeefile, field)))
            print(form.errors)  # Continue to log form errors

    context = {
        'genders': GenderOptions.choices(),
        'form': form,
        'employeefile': employeefile,
        'departments': departments,
        'calendars': calendars,
        'days': days,
        'contribution_codes': ContributionCode.choices(),
        'salarypaymentperiods': salarypaymentperiods,
        'allversions': allversions,
        'employmenttypes': EmploymentType.choices(),  # Pass the enum to the template
        'employee_banks': employee_banks,
        'leave_balances': leave_balances,
        'loans': loans,
        'payroll_groups': payroll_groups,
        'is_latest_non_draft_version': is_latest_non_draft_version(employeefile),
        'draft_eligible': (employeefile.is_draft or employeefile.id != None) # you can create a draft if not already in draft
    }
    return render(request, 'employeefile_edit.html', context)

@permission_required("employee_management.change_employeefile")
def add_employee_bank(request, employee_id):
    employee_file = get_object_or_404(EmployeeFile, id=employee_id)
    form = EmployeeBankForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            employee_bank = form.save(commit=False)
            employee_bank.employeeFile = employee_file
            employee_bank.save()
            return redirect('employeefile_edit_url', id=employee_id)
        else:
            print(form.errors)  # Continue to log form errors


    return render(request, 'add_employee_bank.html',
                  {'form': form,
                   'employee_file': employee_file,
                   'bank_options': BankSwiftCodes.choices(),
                   'supported_currencies': SupportedCurrencies.choices(),
                   'split_types': AmountSplitType.choices()
                   })

@permission_required("employee_management.change_employeefile")
def delete_employee_bank(request, bank_id):
    employee_bank = get_object_or_404(EmployeeBank, id=bank_id)
    employee_id = employee_bank.employeeFile.id
    employee_bank.delete()
    return redirect('employeefile_edit_url', id=employee_id)




@permission_required("employee_management.delete_employeefile" )
def destroy_employeefile(request, id):
  employeefile = EmployeeFile.objects.get(id=id)
  for i in EmployeeFile.objects.filter(employee_code=employeefile.employee_code):
    i.delete()
  return redirect("employeefile_list_url")


@permission_required("employee_management.delete_employeefile" )
def delete_single_emp_record(request, id):
  employeefile = EmployeeFile.objects.get(id=id)
  employeefile.delete()
  return redirect("employeefile_list_url")


@permission_required("employee_management.change_employeefile")
def add_employee_leave_balance(request, employee_id):
    employee_file = get_object_or_404(EmployeeFile, id=employee_id)
    form = EmployeeLeaveBalanceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            leave_balance = form.save(commit=False)
            leave_balance.employeeFile = employee_file
            leave_balance.save()
            return redirect('employeefile_edit_url', id=employee_id)
        else:
            print(form.errors)

    return render(request, 'edit_employee_leave_balance.html',
                  {'form': form,
                   'employee_file': employee_file,
                   'leave_types': LeaveType.choices()})

@permission_required("employee_management.change_employeefile")
def edit_employee_leave_balance(request, leave_balance_id):
    leave_balance = get_object_or_404(EmployeeLeaveBalance, id=leave_balance_id)
    employee_file = leave_balance.employeeFile
    form = EmployeeLeaveBalanceForm(request.POST or None, instance=leave_balance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('employeefile_edit_url', id=leave_balance.employeeFile.id)
        else:
            print(form.errors)

    return render(request, 'edit_employee_leave_balance.html',
                  {'form': form,
                   'employee_file': employee_file,
                   'leave_balance': leave_balance,
                   'leave_types': LeaveType.choices()})

@permission_required("employee_management.change_employeefile")
def delete_employee_leave_balance(request, leave_balance_id):
    leave_balance = get_object_or_404(EmployeeLeaveBalance, id=leave_balance_id)
    employee_id = leave_balance.employeeFile.id
    leave_balance.delete()
    return redirect('employeefile_edit_url', id=employee_id)


@permission_required("employee_management.change_employeefile")
def add_employee_loan(request, employeefile_id):
    employeefile = get_object_or_404(EmployeeFile, id=employeefile_id)
    form = EmployeeLoanForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            loan = form.save(commit=False)
            loan.employeeFile = employeefile
            loan.save()
            return redirect('employeefile_edit_url', id=employeefile_id)
        else:
            print(form.errors)
    return render(request, 'edit_employee_loan.html', {'form': form,'employeefile': employeefile })


@permission_required("employee_management.change_employeefile")
def edit_employee_loan(request, loan_id):
    loan = get_object_or_404(EmployeeLoan, id=loan_id)
    employee_file = loan.employeeFile
    form = EmployeeLoanForm(request.POST or None, instance=loan)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('employeefile_edit_url', id=loan.employeeFile.id)
        else:
            print(form.errors)
    return render(request, 'edit_employee_loan.html', {'form': form, 'employeefile': employee_file, 'loan': loan})


@permission_required("employee_management.change_employeefile")
def delete_employee_loan(request, loan_id):
    loan = get_object_or_404(EmployeeLoan, id=loan_id)
    employeefile_id = loan.employeeFile.id
    loan.delete()
    return redirect('employeefile_edit_url', id=employeefile_id)

@permission_required("employee_management.change_employeefile")
def add_employee_payroll_group(request, employeefile_id):
    employeefile = get_object_or_404(EmployeeFile, id=employeefile_id)
    form = EmployeePayrollGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            payrollgroup = form.save(commit=False)
            payrollgroup.employeeFile = employeefile
            payrollgroup.save()
            return redirect('employeefile_edit_url', id=employeefile_id)
        else:
            print(form.errors)

    return render(request, 'add_employee_payroll_group.html',
                  {'form': form, 'employeefile': employeefile,
                   'payroll_groups': PayrollGroup.objects.all()
                   })

@permission_required("employee_management.change_employeefile")
def delete_employee_payroll_group(request, payroll_group_id):
    payroll_group = get_object_or_404(EmployeePayrollGroup, id=payroll_group_id)
    employeefile_id = payroll_group.employeeFile.id
    payroll_group.delete()
    return redirect('employeefile_edit_url', id=employeefile_id)

class UploadViewEmployeeFile(PermissionRequiredMixin, View):
  permission_required = ("employee_management.add_employeefile")

  def get(self, request, *args, **kwargs):
    return render(request, "upload_employeefile.html", {"form": UploadForm()})

  def post(self, request, *args, **kwargs):
    upload_file = request.FILES["upload_file"]
    rows = TextIOWrapper(upload_file, encoding="utf-8", newline="")
    row_count = 0
    form_errors = []
    for row in DictReader(rows):
      row_count += 1
      form = EmployeeFileForm(row)
      if not form.is_valid():
        form_errors = form.errors
        break
      form.save()
    return render(request, "upload_companycontact.html",
                  {
                    "form": UploadForm(),
                    "form_errors": form_errors,
                    "row_count": row_count,
                  })






