from django import forms
from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget

from django.forms.widgets import MultiWidget

class TimeWidget(forms.TimeInput):
    """Custom time widget that accepts 12-hour format with AM/PM"""
    
    def __init__(self, attrs=None, format='%I:%M %p'):
        final_attrs = {
            'class': 'vTimeField', 
            'size': '10', 
            'placeholder': '02:09 PM',
            'type': 'text'  # Use text input instead of time input
        }
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format)
    
    def format_value(self, value):
        """Format the time value for display in 12-hour format"""
        if value:
            if isinstance(value, str):
                return value
            # Format time as 12-hour with AM/PM
            return value.strftime('%I:%M %p')
        return ''

class DateWidget(AdminDateWidget):
    """Custom date widget"""
    
    def __init__(self, attrs=None, format='%Y-%m-%d'):
        final_attrs = {'class': 'vDateField', 'size': '10'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format)

        

class DateTimeWidget(MultiWidget):
    template_name = 'django/forms/widgets/splitdatetime.html'

    def __init__(self, attrs=None, date_format='%Y-%m-%d', time_format='%I:%M %p'):
        widgets = [
            DateWidget(attrs=attrs, format=date_format),
            TimeWidget(attrs=attrs, format=time_format),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                # Handle string input if needed
                return [None, None]
            return [value.date(), value.time()]
        return [None, None]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['date_label'] = 'Date:'  # Customize as needed
        context['time_label'] = 'Time:'  # Customize as needed
        return context
