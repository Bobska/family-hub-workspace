from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include home app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]

# Only include timesheet URLs if the app is installed (for Docker/production)
if 'timesheet_app' in settings.INSTALLED_APPS:
    urlpatterns.append(path('timesheet/', include('timesheet_app.urls', namespace='timesheet')))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
