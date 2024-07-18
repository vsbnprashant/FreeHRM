from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View

from common.choices import PayrollDeclarationsType, SalaryCalculationsPeriodChoices, PayslipPriningLanguage, \
  EoyBonusOptions, BankSwiftCodes, SupportedCurrencies, TimeUnits, OvertimeCalculationOptions
from .models import PayrollGroup, WorkingCalendar, Department, CompanyContact, CompanyBankAccount, PaymentElement, \
  CompanySettings, CompanyPayrollSettings, CompanyTimesheets


# Create your views here.


def main(request):
  #template = loader.get_template('settings_main.html')
  #return HttpResponse(template.render())
  return render(request, 'settings_main.html', {})


from .forms import PayrollGroupForm, WorkingCalendarForm, DepartmentForm, CompanyContactForm, UploadForm, \
  CompanyBankAccountForm, PaymentElementForm, CompanySettingsForm, CompanyPayrollSettingsForm, CompanyTimesheetsForm
from django.shortcuts import render, redirect, get_object_or_404

@permission_required("settings.view_payrollgroup" )
def payrollgroup_edit(request, id=None):
  if id:
    payrollgroup = get_object_or_404(PayrollGroup, id=id)
    form = PayrollGroupForm(request.POST or None, instance=payrollgroup)
  else:
    form = PayrollGroupForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect('payrollgroup_list')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'form': form,
    'payrollgroup': payrollgroup if id else None
  }
  return render(request, 'payrollgroup_edit.html', context)

@permission_required("settings.delete_payrollgroup" )
def destroy_payroll(request, id):
  payrollgroup = PayrollGroup.objects.get(id=id)
  payrollgroup.delete()
  return redirect("payrollgroup_list")


## Working Calendars

@permission_required("settings.view_workingcalendar" )
def workingcalendar_edit(request, id=None):
  workingcalendar = WorkingCalendar()
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  if id:
    workingcalendar = get_object_or_404(WorkingCalendar, id=id)
    form = WorkingCalendarForm(request.POST or None, instance=workingcalendar)
  else:
    form = WorkingCalendarForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect('workingcalendar_list_url')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'form': form,
    'workingcalendar': workingcalendar,
    'days': days
  }
  return render(request, 'workingcalendar_edit.html', context)

@permission_required("settings.delete_workingcalendar" )
def destroy_workingcalendar(request, id):
  workingcalendar = WorkingCalendar.objects.get(id=id)
  workingcalendar.delete()
  return redirect("workingcalendar_list_url")




## Departments

@permission_required("settings.view_department" )
def department_tree_view(request):
    root_departments = Department.objects.filter(parent_department__isnull=True)
    return render(request, 'department_tree.html', {'departments': root_departments})


@permission_required("settings.view_department")
def department_edit(request, id=None):
  parents = Department.objects.all()

  if id:
    parents = list(filter(lambda x: (x.id != id), parents))
    department = get_object_or_404(Department, id=id)
    form = DepartmentForm(request.POST or None, instance=department)
  else:
    form = DepartmentForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect('department_list_url')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'form': form,
    'department': department if id else None,
    'parents': parents
  }
  return render(request, 'department_edit.html', context)

@permission_required("settings.delete_department" )
def destroy_department(request, id):
  department = Department.objects.get(id=id)
  department.delete()
  return redirect("department_list_url")



##Company Contacts

@permission_required("settings.view_companycontact" )
def companycontact_edit(request, id=None):
  if id:
    companycontact = get_object_or_404(CompanyContact, id=id)
    form = CompanyContactForm(request.POST or None, instance=companycontact)
  else:
    form = CompanyContactForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect('companycontact_list_url')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'form': form,
    'companycontact': companycontact if id else None
  }
  return render(request, 'companycontact_edit.html', context)

@permission_required("settings.delete_companycontact" )
def destroy_companycontact(request, id):
  companycontact = CompanyContact.objects.get(id=id)
  companycontact.delete()
  return redirect("companycontact_list_url")


class UploadViewCompanyContact(PermissionRequiredMixin, View):
  permission_required = ("companycontact.add_companycontact")

  def get(self, request, *args, **kwargs):
    return render(request, "upload_companycontact.html", {"form": UploadForm()})

  def post(self, request, *args, **kwargs):
    upload_file = request.FILES["upload_file"]
    rows = TextIOWrapper(upload_file, encoding="utf-8", newline="")
    row_count = 0
    form_errors = []
    for row in DictReader(rows):
      row_count += 1
      form = CompanyContactForm(row)
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





## Company Bank Accounts

@permission_required("settings.view_companybankaccount" )
def companybankaccount_edit(request, id=None):
  parents = CompanyBankAccount.objects.all()

  if id:
    companybankaccount = get_object_or_404(CompanyBankAccount, id=id)
    form = CompanyBankAccountForm(request.POST or None, instance=companybankaccount)
  else:
    form = CompanyBankAccountForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect('companybankaccount_list_url')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'bank_options': BankSwiftCodes.choices(),
    'supported_currencies' : SupportedCurrencies.choices(),
    'form': form,
    'companybankaccount': companybankaccount if id else None,
  }
  return render(request, 'companybankaccount_edit.html', context)

@permission_required("settings.delete_companybankaccount" )
def destroy_companybankaccount(request, id):
  companybankaccount = CompanyBankAccount.objects.get(id=id)
  companybankaccount.delete()
  return redirect("companybankaccount_list_url")




## Payment Elements

@permission_required("settings.view_paymentelement" )
def paymentelement_edit(request, id=None):

  if id:
    paymentelement = get_object_or_404(PaymentElement, id=id)
    form = PaymentElementForm(request.POST or None, instance=paymentelement)
  else:
    form = PaymentElementForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      # This will prepare the new payment element without saving it to the database
      new_paymentelement = form.save(commit=False)

      # Reset the ID to None to create a new object
      new_paymentelement.id = None

      # Now save the new payment element to the database
      new_paymentelement.save()

      f = form.save()

      if f.origin is None:
            f.origin = f
            f.save()
      else:
            f.origin =f.origin
            f.save()
      return redirect('paymentelement_list_url')
    else:
      # If the form is not valid, print errors in the console (can be modified based on requirements)
       print(form.errors)

  context = {
    'form': form,
    'paymentelement': paymentelement if id else None,
  }
  return render(request, 'paymentelement_edit.html', context)

@permission_required("settings.delete_paymentelement" )
def destroy_paymentelement(request, id):
  paymentelement = PaymentElement.objects.get(id=id)
  for i in PaymentElement.objects.filter(code=paymentelement.code):
    i.delete()
  return redirect("paymentelement_list_url")


@permission_required("settings.view_paymentelement")
def details(request, id):
    paymentelement = PaymentElement.objects.get(id=id)
    allversions = PaymentElement.objects.filter(code=paymentelement.code)
    template = loader.get_template('paymentelement_details.html')
    context = {
        'paymentelement': paymentelement,
         'allversions': allversions
    }
    return HttpResponse(template.render(context, request))


@permission_required("settings.view_companysettings")
def edit_company_settings(request):
  # Since this is a singleton model, we retrieve the single instance or create it if it does not exist.
  companysettings = CompanySettings.load_without_saving()
  print(companysettings)

  if request.method == "POST":
    # We use the instance to populate the form with the existing data.
    form = CompanySettingsForm(request.POST, instance=companysettings)
    if form.is_valid():
      # Save the settings if the form is valid.
      form.save()
      # Redirect to a success page, dashboard, or wherever is appropriate after saving.
      return redirect('settings_main')
    else:
      print(form.errors)
  else:
    # If this is a GET request, we just display the form with the existing settings instance.
    form = CompanySettingsForm(instance=companysettings)

  return render(request, 'edit_company_settings.html', {'form': form, 'companysettings': companysettings})


@permission_required("settings.view_companypayrollsettings")
def edit_company_payroll_settings(request):
  choices = [(choice.value[0], choice.value[1]) for choice in SalaryCalculationsPeriodChoices]
  languages = [(lan.value[0], lan.value[1]) for lan in PayslipPriningLanguage]
  # Since this is a singleton model, we retrieve the single instance or create it if it does not exist.
  companypayrollsettings = CompanyPayrollSettings.load_without_saving()

  if request.method == "POST":
    # We use the instance to populate the form with the existing data.
    form = CompanyPayrollSettingsForm(request.POST, instance=companypayrollsettings)
    if form.is_valid():
      # Save the settings if the form is valid.
      form.save()
      # Redirect to a success page, dashboard, or wherever is appropriate after saving.
      return redirect('settings_main')
    else:
      print(form.errors)
  else:
    # If this is a GET request, we just display the form with the existing settings instance.
    form = CompanyPayrollSettingsForm(instance=companypayrollsettings)

  return render(request, 'edit_company_payroll_settings.html', {
    'languages': languages,
    'eoy_bonus_options': EoyBonusOptions.choices(),
    'choices': choices,'declarations_types': PayrollDeclarationsType.choices(),
    'form': form, 'companypayrollsettings': companypayrollsettings})





@permission_required("settings.view_companytimesheets")
def edit_company_timesheets(request):
  # Since this is a singleton model, we retrieve the single instance or create it if it does not exist.
  companytimesheets = CompanyTimesheets.load_without_saving()

  if request.method == "POST":
    # We use the instance to populate the form with the existing data.
    form = CompanyTimesheetsForm(request.POST, instance=companytimesheets)
    if form.is_valid():
      # Save the settings if the form is valid.
      form.save()
      # Redirect to a success page, dashboard, or wherever is appropriate after saving.
      return redirect('settings_main')
    else:
      print(form.errors)
  else:
    # If this is a GET request, we just display the form with the existing settings instance.
    form = CompanyTimesheetsForm(instance=companytimesheets)

  return render(request, 'edit_company_timesheets_settings.html',
                {
                  'timeunits': TimeUnits.choices(),
                  'overtimecalculationoptions': OvertimeCalculationOptions.choices(),
                  'form': form,
                 'companytimesheets': companytimesheets})




