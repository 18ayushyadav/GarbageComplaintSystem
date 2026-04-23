"""
Smart Garbage Complaint System — Project URL Configuration

This is the root URL configuration that routes all incoming requests.
- '/' routes go to the complaints app
- '/admin/' routes to Django's built-in admin panel
- Media files are served in development mode
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin panel — accessible at /admin/
    path('admin/', admin.site.urls),

    # All complaint-related URLs are handled by the complaints app
    path('', include('complaints.urls')),
]

# ─── Serve media files during development ────────────────────────────────────
# In production, use a web server (Nginx/Apache) to serve media files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
