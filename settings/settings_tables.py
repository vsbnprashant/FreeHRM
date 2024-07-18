from .models import PayrollGroup, CompanyContact, CompanyBankAccount, PaymentElement
from  .models import Department
from  .models import WorkingCalendar
from django.db.models import Max, OuterRef, Subquery, F
import django_tables2 as tables
from django_tables2 import TemplateColumn
from django_tables2.utils import A
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_tables2.export.views import ExportMixin

class PayrollGroupTable(tables.Table):
        name = tables.Column(linkify={"viewname": "payrollgroup_edit", "args": [tables.A("pk")]})
        Actions = TemplateColumn(
            template_code='{% if perms.settings.view_payrollgroup %} <a href="{% url "payrollgroup_edit" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.settings.delete_payrollgroup %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');" href="{% url "payrollgroup_delete" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
        , orderable=False)

        class Meta:
            model = PayrollGroup
            attrs = {"class": "table"}


class PayrollGroupTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("settings.payrollgroup_view")
    table_class = PayrollGroupTable
    queryset = PayrollGroup.objects.all()
    template_name = "payrollgroup_datatable.html"


class WorkingCalendarTable(tables.Table):
        name = tables.Column(linkify={"viewname": "workingcalendar_edit_url", "args": [tables.A("pk")]})
        Actions = TemplateColumn(
            template_code='{% if perms.settings.view_workingcalendar %} <a href="{% url "workingcalendar_edit_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.settings.delete_workingcalendar %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');" href="{% url "workingcalendar_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
            , orderable=False)

        class Meta:
            model = WorkingCalendar
            attrs = {"class": "table"}
            exclude = ('monday_working', 'monday_start_time', 'monday_end_time', 'monday_overtime', 'tuesday_working', 'tuesday_start_time', 'tuesday_end_time', 'tuesday_overtime', 'wednesday_working', 'wednesday_start_time', 'wednesday_end_time', 'wednesday_overtime', 'thursday_working', 'thursday_start_time', 'thursday_end_time', 'thursday_overtime', 'friday_working', 'friday_start_time', 'friday_end_time', 'friday_overtime', 'saturday_working', 'saturday_start_time', 'saturday_end_time', 'saturday_overtime', 'sunday_working', 'sunday_start_time', 'sunday_end_time', 'sunday_overtime', 'lateness_minimum_minutes', 'overtime_minimum_minutes', 'overtime_deduct_lateness', 'overtime_minimum_arrival_minutes', 'overtime_after_hours_break', 'overtime_after_mins')


class WorkingCalendarTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("settings.workingcalendar_view")
    table_class = WorkingCalendarTable
    queryset = WorkingCalendar.objects.all()
    template_name = "workingcalendar_datatable.html"




class DepartmentTable(tables.Table):
        name = tables.Column(linkify={"viewname": "department_edit_url", "args": [tables.A("pk")]})
        parent_department = tables.Column(linkify={"viewname": "department_edit_url", "args": [tables.A("parent_department__pk")]}, accessor="parent_department__name", verbose_name='Parent')
        Actions = TemplateColumn(
            template_code='{% if perms.settings.view_department %} <a href="{% url "department_edit_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.settings.delete_department %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');" href="{% url "department_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
        , orderable=False)
        class Meta:
            model = Department
            attrs = {"class": "table"}


class DepartmentTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("settings.department_view")
    table_class = DepartmentTable
    queryset = Department.objects.all()
    template_name = "department_datatable.html"





class CompanyContactTable(tables.Table):
        name = tables.Column(linkify={"viewname": "companycontact_edit_url", "args": [tables.A("pk")]})
        Actions = TemplateColumn(
            template_code='{% if perms.settings.view_companycontact %} <a href="{% url "companycontact_edit_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.settings.delete_companycontact %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');" href="{% url "companycontact_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
        , orderable=False)

        class Meta:
            model = CompanyContact
            attrs = {"class": "table"}


class CompanyContactTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("settings.companycontact_view")
    table_class = CompanyContactTable
    queryset = CompanyContact.objects.all()
    template_name = "companycontact_datatable.html"

class CompanyBankAccountTable(tables.Table):
        name = tables.Column(linkify={"viewname": "companybankaccount_edit_url", "args": [tables.A("pk")]})
        Actions = TemplateColumn(
            template_code='{% if perms.settings.view_companybankaccount %} <a href="{% url "companybankaccount_edit_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.settings.delete_companybankaccount %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');" href="{% url "companybankaccount_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
            , orderable=False)

        class Meta:
            model = CompanyBankAccount
            attrs = {"class": "table"}


class CompanyBankAccountTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
        permission_required = ("settings.companybankaccount_view")
        table_class = CompanyBankAccountTable
        queryset = CompanyBankAccount.objects.all()
        template_name = "companybankaccount_datatable.html"


class PaymentElementTable(tables.Table):
    Actions = TemplateColumn(
        template_code='{% if perms.settings.view_paymentelement %} <a href="{% url "paymentelement_edit_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                      '{% if perms.settings.delete_paymentelement %} <a onclick="return confirm(\'Are you sure you want to delete this PaymentElement and All related Versions?\');" href="{% url "paymentelement_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
                      '{% if perms.settings.view_paymentelement %} <a  href="{% url "paymentelement_view_url" record.id %}">See Details and previous versions </a> {% endif %}'
        , orderable=False)

    class Meta:
        model = PaymentElement
        attrs = {"class": "table"}


class PaymentElementTableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("settings.paymentelement_view")
    table_class = PaymentElementTable
    #queryset = PaymentElement.objects.all()
    # First, we'll make a subquery to get the maximum version number for each code.
    max_versions = PaymentElement.objects.values('code').annotate(max_version=Max('version')).values('max_version')

    # Now, we filter the original queryset to get only the items with a version number
    # that matches the maximum version for that code.
    queryset = PaymentElement.objects.annotate(
        max_version=Subquery(
            PaymentElement.objects.filter(
                code=OuterRef('code')
            ).values('code').annotate(
                max_version=Max('version')
            ).values('max_version')[:1]
        )
    ).filter(
        version=F('max_version')
    )

    # Now, 'queryset' contains only the PaymentElements with the maximum version for each code.
    template_name = "paymentelement_datatable.html"

