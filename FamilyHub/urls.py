"""
FamilyHub Main URL Configuration

URL patterns for the main FamilyHub application.
Follows Django best practices with proper namespacing.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Home app URLs (includes dashboard and core functionality)
    path('', include('home.urls')),
    
    # Future: App URLs will be added here as they are integrated
    # path('timesheet/', include('apps.timesheet_app.urls')),
    # path('budget/', include('apps.household_budget_app.urls')),
    # path('daycare/', include('apps.daycare_invoice_app.urls')),
    # path('employment/', include('apps.employment_history_app.urls')),
    # path('payments/', include('apps.upcoming_payments_app.urls')),
    # path('creditcards/', include('apps.credit_card_mgmt_app.urls')),
]

# Development static file serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)