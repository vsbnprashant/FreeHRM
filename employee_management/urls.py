from django.urls import path
from . import views
from .mytables import TableView, EmployeeFileTableView, EmployeeFileTableView_DraftsOnly
from .views import UploadView, UploadViewEmployeeFile, add_employee_leave_balance

urlpatterns = [
    path('', views.main, name='main'),
    #path('locations/', views.locations, name='locations_home'),
    #path('locations/details/<int:id>', views.details, name='locations_details'),
    path('locations/list',TableView.as_view(), name='locations_list'),

    path('locations/new', views.location_edit, name='locations_create'),
    path('locations/edit/<int:id>', views.location_edit, name='locations_edit'),

    path('locations/delete/<int:id>', views.destroy, name='locations_delete'),
    path('locations/upload/',  UploadView.as_view(), name='locations_import_url'),

    path('employeefile/list', EmployeeFileTableView.as_view(), name='employeefile_list_url'),
    path('employeefile/list/drafts', EmployeeFileTableView_DraftsOnly.as_view(), name='employeefile_list_draft_url'),

    path('employeefile/new/', views.employeefile_edit, name='employeefile_create_url'),
    path('employeefile/new/<int:id>/', views.employee_create_new_version, name='employeefile_create_new_version_url'),
    path('employeefile/edit/<int:id>', views.employeefile_edit, name='employeefile_edit_url'),
    path('employeefile/latestvalid/<int:id>/', views.get_latest_non_draft_version, name='employeefile_see_latest_valid_url'),

    path('employeefile/delete/<int:id>', views.destroy_employeefile, name='employeefile_delete_url'),
    path('employeefile/delete_single/<int:id>', views.delete_single_emp_record, name='employeefile_delete_single_url'),

    path('employeefile/upload/', UploadViewEmployeeFile.as_view(), name='employeefile_import_url'),
    path('employeefile/add-bank/<int:employee_id>/', views.add_employee_bank, name='add_employee_bank'),
    path('employeefile/delete-bank/<int:bank_id>/', views.delete_employee_bank, name='delete_employee_bank'),
    path('employeefile/add-leave-balance/<int:employee_id>/', views.add_employee_leave_balance, name='add_employee_leave_balance'),
    path('employeefile/edit-leave-balance/<int:leave_balance_id>/', views.edit_employee_leave_balance,name='edit_employee_leave_balance'),
    path('employeefile/delete-leave-balance/<int:leave_balance_id>/', views.delete_employee_leave_balance,name='delete_employee_leave_balance'),

    path('employeefile/add-loan/<int:employeefile_id>/', views.add_employee_loan,
         name='add_employee_loan'),
    path('employeefile/edit-loan/<int:loan_id>/', views.edit_employee_loan,
         name='edit_employee_loan'),
    path('employeefile/delete-loan/<int:loan_id>/', views.delete_employee_loan,
         name='delete_employee_loan'),

    path('employeefile/add-payrollgroup/<int:employeefile_id>/', views.add_employee_payroll_group,
         name='add_employee_payroll_group'),
    path('employeefile/delete-payrollgroup/<int:payroll_group_id>/', views.delete_employee_payroll_group,
         name='delete_employee_payroll_group'),



]

