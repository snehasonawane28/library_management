from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils import timezone
from datetime import datetime, time
from .models import Book, BorrowRecord
from .admin_forms import DateWidget, TimeWidget


# Apply the custom time format to all admin models
class CustomAdminSite(admin.AdminSite):
    site_header = 'Library Management Admin'
    site_title = 'Library Admin'
    index_title = 'Welcome to Library Admin'
    change_form_template = 'admin/time.html'

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register all models with the custom admin site
class BorrowRecordAdminForm(forms.ModelForm):
    # Override time fields to accept 12-hour format
    borrow_time = forms.TimeField(
        required=False,
        input_formats=[
            '%I:%M %p',      # 02:09 PM
            '%I:%M%p',       # 02:09PM (no space)
            '%I:%M:%S %p',   # 02:09:30 PM
            '%H:%M:%S',      # 14:09:30 (24-hour fallback)
            '%H:%M',         # 14:09 (24-hour fallback)
        ],
        widget=TimeWidget(),
        help_text='Enter time in format: 02:09 PM'
    )
    due_time = forms.TimeField(
        required=False,
        input_formats=[
            '%I:%M %p',      # 02:09 PM
            '%I:%M%p',       # 02:09PM (no space)
            '%I:%M:%S %p',   # 02:09:30 PM
            '%H:%M:%S',      # 14:09:30 (24-hour fallback)
            '%H:%M',         # 14:09 (24-hour fallback)
        ],
        widget=TimeWidget(),
        help_text='Enter time in format: 02:09 PM'
    )
    return_time = forms.TimeField(
        required=False,
        input_formats=[
            '%I:%M %p',      # 02:09 PM
            '%I:%M%p',       # 02:09PM (no space)
            '%I:%M:%S %p',   # 02:09:30 PM
            '%H:%M:%S',      # 14:09:30 (24-hour fallback)
            '%H:%M',         # 14:09 (24-hour fallback)
        ],
        widget=TimeWidget(),
        help_text='Enter time in format: 02:09 PM'
    )
    
    class Meta:
        model = BorrowRecord
        fields = '__all__'
        widgets = {
            'borrow_date': DateWidget(),
            'due_date': DateWidget(),
            'return_date': DateWidget(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set current date/time as default for new records
        if not self.instance.pk:
            now = timezone.localtime(timezone.now())
            self.initial['borrow_date'] = now.date()
            self.initial['borrow_time'] = now.time()
            # Set default due date to 14 days from now
            due_datetime = now + timezone.timedelta(days=14)
            self.initial['due_date'] = due_datetime.date()
            self.initial['due_time'] = now.time()

    def clean_borrow_time(self):
        """Ensure borrow_time is set"""
        borrow_time = self.cleaned_data.get('borrow_time')
        if not borrow_time and self.cleaned_data.get('borrow_date'):
            # Default to current time if not provided
            return timezone.localtime(timezone.now()).time()
        return borrow_time
    
    def clean_due_time(self):
        """Ensure due_time is set"""
        due_time = self.cleaned_data.get('due_time')
        if not due_time and self.cleaned_data.get('due_date'):
            # Default to current time if not provided
            return timezone.localtime(timezone.now()).time()
        return due_time


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('title', 'author', 'isbn')

class BorrowRecordAdmin(admin.ModelAdmin):
    form = BorrowRecordAdminForm
    list_display = ('book', 'user', 'get_borrow_datetime', 'get_due_datetime', 'get_return_datetime', 'fine_amount', 'fine_paid')
    list_filter = ('fine_paid', 'borrow_date', 'due_date')
    search_fields = ('book__title', 'user__username')
    date_hierarchy = 'borrow_date'
    
    def get_borrow_datetime(self, obj):
        if obj.borrow_date and obj.borrow_time:
            return f"{obj.borrow_date} {obj.borrow_time.strftime('%I:%M %p')}"
        return ""
    get_borrow_datetime.short_description = 'Borrowed On'
    get_borrow_datetime.admin_order_field = 'borrow_date'
    
    def get_due_datetime(self, obj):
        if obj.due_date and obj.due_time:
            return f"{obj.due_date} {obj.due_time.strftime('%I:%M %p')}"
        return ""
    get_due_datetime.short_description = 'Due On'
    get_due_datetime.admin_order_field = 'due_date'
    
    def get_return_datetime(self, obj):
        if obj.return_date and obj.return_time:
            return f"{obj.return_date} {obj.return_time.strftime('%I:%M %p')}"
        return "-"
    get_return_datetime.short_description = 'Returned On'
    get_return_datetime.admin_order_field = 'return_date'

class CustomAdminSite(admin.AdminSite):
    site_header = 'Library Management Admin'
    site_title = 'Library Admin'
    index_title = 'Welcome to Library Admin'

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models with custom admin site
custom_admin_site.register(Book, BookAdmin)
custom_admin_site.register(BorrowRecord, BorrowRecordAdmin)
custom_admin_site.register(Group)
custom_admin_site.register(User)