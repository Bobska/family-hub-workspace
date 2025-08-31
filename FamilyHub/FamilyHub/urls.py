from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .app_registry import get_dynamic_url_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include home app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]

# Add dynamic app URLs
dynamic_apps = get_dynamic_url_patterns()
for url_pattern, include_path, namespace in dynamic_apps:
    try:
        urlpatterns.append(path(url_pattern, include(include_path, namespace=namespace)))
    except ImportError as e:
        # App URLs not available, skip silently in production
        if settings.DEBUG:
            print(f"Warning: Could not load URLs for {namespace}: {e}")

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
