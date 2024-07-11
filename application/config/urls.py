from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("", include("public.urls")),
    path("", include("apps.user.urls")),
    path("", include("apps.post.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += (
        [path("admin/", admin.site.urls)]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
