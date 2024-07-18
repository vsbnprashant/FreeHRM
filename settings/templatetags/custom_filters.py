from django import template

register = template.Library()

@register.filter
def is_working_checked(workingcalendar, day):
    attr = day.lower() + '_working'
    return getattr(workingcalendar, attr, False) if workingcalendar.id else False

@register.filter
def is_overtime_checked(workingcalendar, day):
    attr = day.lower() + '_overtime'
    return getattr(workingcalendar, attr, False) if workingcalendar.id else False

@register.filter(name='get_start_time_attr')
def get_time_attr(workingcalendar, arg):
    """Retrieve and format a time attribute of an object dynamically by day."""
    attr_name = f"{arg.lower()}_start_time"
    time_value = getattr(workingcalendar, attr_name, None)
    if time_value:
        return time_value.strftime('%H:%M:%S')
    return "08:00"  # default time if not set

@register.filter(name='get_end_time_attr')
def get_time_attr(workingcalendar, arg):
    """Retrieve and format a time attribute of an object dynamically by day."""
    attr_name = f"{arg.lower()}_end_time"
    time_value = getattr(workingcalendar, attr_name, None)
    if time_value:
        return time_value.strftime('%H:%M:%S')
    return "17:00"  # default time if not set


@register.filter(name='add_class')
def add_class(value, arg):
    """Adds CSS classes to Django form fields."""
    return value.as_widget(attrs={'class': arg})
