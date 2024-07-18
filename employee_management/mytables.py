from django.db.models import Subquery, OuterRef, Max, F

from .models import Location, EmployeeFile
import django_tables2 as tables
from django_tables2 import TemplateColumn
from django_tables2.utils import A
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_tables2.export.views import ExportMixin
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class LocationTable(tables.Table):
        location = tables.Column(linkify={"viewname": "locations_edit", "args": [tables.A("pk")]})
        Actions = TemplateColumn(
            template_code='{% if perms.employee_management.view_location %} <a href="{% url "locations_edit" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
                          '{% if perms.employee_management.delete_location %} <a onclick="return confirm(\'Are you sure you want to delete this item?\');"  href="{% url "locations_delete" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}', orderable=False)

        class Meta:
            model = Location
            attrs = {"class": "table"}


class TableView(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("employee_management.view_location")
    table_class = LocationTable
    queryset = Location.objects.all()
    template_name = "datatable.html"



class EmployeeFileTable(tables.Table):
    Actions = TemplateColumn(
        template_code='{% if perms.employee_management.view_employeefile %} <a href="{% url "employeefile_edit_url" record.id %}" {% if record.is_draft %} class="btn btn-outline-danger" {% else %} class="btn btn-success" {% endif %} ><i class="bi bi-file-earmark"></i></a> {% endif %}'
                      '{% if perms.employee_management.delete_employeefile %} <a onclick="return confirm(\'Are you sure you want to delete this Employee File and All related Versions?\');" href="{% url "employeefile_delete_url" record.id %}" class="btn btn-danger"><i class="bi bi-trash"></i></a> {% endif %}'
                      '{% if perms.employee_management.change_employeefile and record.is_draft and record.version != 1 %} <a href="{% url "employeefile_see_latest_valid_url" record.id %}" class="btn btn-success"><i class="bi bi-file-earmark"></i></a> {% endif %}'
        , orderable=False)
    class Meta:
        model = EmployeeFile
        attrs = {"class": "table"}
        exclude = ('reason_of_departure',"suspension_date", "reason_for_suspension", 'monday_working', 'tuesday_working',
                   'wednesday_working', 'thursday_working', 'friday_working', 'saturday_working', 'sunday_working', 'monday_overtime',
                   'tuesday_overtime', 'wednesday_overtime', 'thursday_overtime', 'friday_overtime', 'saturday_overtime', 'sunday_overtime',
                   "tan", "pension_fund_number", "origin",
                    'is_draft')
        sequence = ('Actions','is_draft', '...', 'active_employee')

### Other attributes
#"last_name", "first_name", "other_names", "maiden_name", "nic",
#                   "gender", "employee_code", "badge_access_control_number", "mobile_number", "phone",
#                   "postcode", "date_joined", "in_current_position_since", "post", "employment_type",
#                   "calendar", "department", "office_site", "departure_date",
# "salary_payment_interval", "paye_income_tax_enabled",
#   "npf_nsf_contribution_enabled", "contribution_code", "paid_by_bank_transfer",
###
class EmployeeNameFilter(FilterSet):
    class Meta:
        model = EmployeeFile
        fields = {"last_name": ["exact", "contains"], "first_name": ["exact", "contains"]}

class EmployeeFileTableView(ExportMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = ("employee_management.employeefile_view")
    table_class = EmployeeFileTable
    #queryset = EmployeeFile.objects.all()
    # First, we'll make a subquery to get the maximum version number for each code.
    max_versions = EmployeeFile.objects.values('employee_code').annotate(max_version=Max('version')).values('max_version')

    # Now, we filter the original queryset to get only the items with a version number
    # that matches the maximum version for that code.
    queryset = EmployeeFile.objects.annotate(
        max_version=Subquery(
            EmployeeFile.objects.filter(
                employee_code=OuterRef('employee_code')
            ).values('employee_code').annotate(
                max_version=Max('version')
            ).values('max_version')[:1]
        )
    ).filter(
        version=F('max_version')
    )

    # Now, 'queryset' contains only the PaymentElements with the maximum version for each code.
    template_name = "employeefile_datatable.html"
    filterset_class = EmployeeNameFilter


## FIXME Not yet used
class EmployeeFileTableView_DraftsOnly(ExportMixin, PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ("employee_management.employeefile_view")
    table_class = EmployeeFileTable
    queryset = EmployeeFile.objects.filter(is_draft=True)


    # Now, 'queryset' contains only the PaymentElements with the maximum version for each code.
    template_name = "employeefile_datatable.html"
