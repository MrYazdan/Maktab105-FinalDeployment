from django.urls import path, include

urlpatterns = [
    path("auth/", include("apps.user.urls.auth")),
    path("user/", include("apps.user.urls.user")),
]
