from django.urls import path

from settings import views
from settings.settings_tables import PayrollGroupTable, PayrollGroupTableView, WorkingCalendarTableView, \
    DepartmentTableView, CompanyContactTableView, CompanyBankAccountTableView, PaymentElementTableView
from settings.views import UploadViewCompanyContact

urlpatterns = [
    path('', views.main, name='settings_main'),

    path('payrollgroup/list', PayrollGroupTableView.as_view(), name='payrollgroup_list'),
    path('payrollgroup/new', views.payrollgroup_edit, name='payrollgroup_create'),
    path('payrollgroup/edit/<int:id>', views.payrollgroup_edit, name='payrollgroup_edit'),
    path('payrollgroup/delete/<int:id>', views.destroy_payroll, name='payrollgroup_delete'),

    path('workingcalendar/list', WorkingCalendarTableView.as_view(), name='workingcalendar_list_url'),
    path('workingcalendar/new', views.workingcalendar_edit, name='workingcalendar_create_url'),
    path('workingcalendar/edit/<int:id>', views.workingcalendar_edit, name='workingcalendar_edit_url'),
    path('workingcalendar/delete/<int:id>', views.destroy_workingcalendar, name='workingcalendar_delete_url'),

    path('department/list', DepartmentTableView.as_view(), name='department_list_url'),
    path('department/new', views.department_edit, name='department_create_url'),
    path('department/edit/<int:id>', views.department_edit, name='department_edit_url'),
    path('department/delete/<int:id>', views.destroy_department, name='department_delete_url'),
    path('departments/treeview', views.department_tree_view, name='department_tree'),


    path('companycontact/list', CompanyContactTableView.as_view(), name='companycontact_list_url'),
    path('companycontact/new', views.companycontact_edit, name='companycontact_create_url'),
    path('companycontact/edit/<int:id>', views.companycontact_edit, name='companycontact_edit_url'),
    path('companycontact/delete/<int:id>', views.destroy_companycontact, name='companycontact_delete_url'),
    path('companycontact/upload/', UploadViewCompanyContact.as_view(), name='companycontact_import_url'),

    path('companybankaccount/list', CompanyBankAccountTableView.as_view(), name='companybankaccount_list_url'),
    path('companybankaccount/new', views.companybankaccount_edit, name='companybankaccount_create_url'),
    path('companybankaccount/edit/<int:id>', views.companybankaccount_edit, name='companybankaccount_edit_url'),
    path('companybankaccount/delete/<int:id>', views.destroy_companybankaccount, name='companybankaccount_delete_url'),

    path('paymentelement/list', PaymentElementTableView.as_view(), name='paymentelement_list_url'),
    path('paymentelement/new', views.paymentelement_edit, name='paymentelement_create_url'),
    path('paymentelement/edit/<int:id>', views.paymentelement_edit, name='paymentelement_edit_url'),
    path('paymentelement/delete/<int:id>', views.destroy_paymentelement, name='paymentelement_delete_url'),
    path('paymentelement/details/<int:id>', views.details, name='paymentelement_view_url'),

    path('companysettings/edit', views.edit_company_settings, name='edit_company_settings_url'),
    path('companypayrollsettings/edit', views.edit_company_payroll_settings, name='edit_company_payroll_settings_url'),
    path('companytimesheetsettings/edit', views.edit_company_timesheets, name='edit_company_timesheets_settings_url'),

]

