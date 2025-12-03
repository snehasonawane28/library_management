# library_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from library_app.admin_custom import custom_admin_site

# Set the default admin site to our custom admin site
admin.site = custom_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
