from django.contrib import admin
from .models import Location, EmployeePayrollGroup, EmployeeLoan, EmployeeEDFDetails, EmployeeLeaveBalance, \
  EmployeeBank, EmployeeFile


# Register your models here.


#admin.site.register(Location)


class LocationAdmin(admin.ModelAdmin):
  list_display = ("location", "country", "city")

admin.site.register(Location, LocationAdmin)


class EmployeePayrollGroupAdmin(admin.ModelAdmin):
  list_display = ("employeeFile", "payrollGroup")

admin.site.register(EmployeePayrollGroup, EmployeePayrollGroupAdmin)


class EmployeeLoanAdmin(admin.ModelAdmin):
  list_display = ("employee_loan_code", "employeeFile", "loan_amount")


admin.site.register(EmployeeLoan, EmployeeLoanAdmin)


class EmployeeEDFDetailsAdmin(admin.ModelAdmin):
  list_display = ("employeeFile", "edf_income_threshold", "total_amount_exemption")


admin.site.register(EmployeeEDFDetails, EmployeeEDFDetailsAdmin)


class EmployeeLeaveBalanceAdmin(admin.ModelAdmin):
  list_display = ("employeeFile", "leave_code", "amount", "available")


admin.site.register(EmployeeLeaveBalance, EmployeeLeaveBalanceAdmin)


class EmployeeFileAdmin(admin.ModelAdmin):
  list_display = ("last_name", "first_name", "employee_code")


admin.site.register(EmployeeFile, EmployeeFileAdmin)


class EmployeeBankAdmin(admin.ModelAdmin):
  list_display = ("employeeFile", "bank_code", "account_number")



