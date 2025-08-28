from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import home_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_dashboard, name='home'),  # Root URL goes to dashboard
    path('home/', include('home.urls')),
    
    # Include standalone app URLs (will add these as we develop each app)
    # path('timesheet/', include('timesheet_app.urls')),
    # path('budget/', include('household_budget_app.urls')),
    # path('daycare/', include('daycare_invoice_app.urls')),
    # path('employment/', include('employment_history_app.urls')),
    # path('payments/', include('upcoming_payments_app.urls')),
    # path('creditcards/', include('credit_card_mgmt_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)