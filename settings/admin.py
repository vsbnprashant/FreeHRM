from django.contrib import admin
from .models import PayrollGroup, WorkingCalendar, Department, CompanySettings, CompanyContact, CompanyPayrollSettings, CompanyBankAccount, CompanyTimesheets, PaymentElement

class PayrollGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

admin.site.register(PayrollGroup, PayrollGroupAdmin)

class WorkingCalendarAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(WorkingCalendar, WorkingCalendarAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name","parent_department")

admin.site.register(Department, DepartmentAdmin)

class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "shortname", "tan", "npf", "brn", "nature_of_business", "incorporation_date")

admin.site.register(CompanySettings, CompanySettingsAdmin)

class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "address_line1", "address_line2", "phone", "city", "email", "latitude", "longitude", "distance_range", "primary")

admin.site.register(CompanyContact, CompanyContactAdmin)

class CompanyPayrollSettingsAdmin(admin.ModelAdmin):
    list_display = ("period_closing_day_of_month", "period_pay_day", "declarations_type", "payslip_template", "payslip_printing_language", "salary_calculations_period", "eoy_bonus")

admin.site.register(CompanyPayrollSettings, CompanyPayrollSettingsAdmin)

class CompanyBankAccountAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "branch", "account_number", "iban", "code", "currency", "default_bank")

admin.site.register(CompanyBankAccount, CompanyBankAccountAdmin)

class CompanyTimesheetsAdmin(admin.ModelAdmin):
    list_display = ("allow_time_input_from_employee", "automatic_lateness", "lateness_field", "lateness_calculation_type", "lateness_absence_field", "automatic_overtime", "overtime_field", "overtime_calculation_type", "overtime_calculation_option")

admin.site.register(CompanyTimesheets, CompanyTimesheetsAdmin)

class PaymentElementAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "formula", "order", "version", "origin")

admin.site.register(PaymentElement, PaymentElementAdmin)

