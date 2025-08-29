from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Temporarily commented out for basic testing
# from .health_views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include home app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('timesheet/', include('timesheet.urls')),  # Shared timesheet app
    
    # Health check endpoints
    # Temporarily commented out for basic testing
    # path('health/', health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
