"""
URL configuration for jnab_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Admin Site Branding
admin.site.site_header = "JNAB Innovations · Command Center"
admin.site.site_title = "JNAB Admin Portal"
admin.site.index_title = "Lead Management, Recruitment & Academy Admissions"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

# Serve media files (uploaded resumes, documents) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
