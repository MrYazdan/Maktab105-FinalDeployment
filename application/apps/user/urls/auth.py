from django.urls import path
from apps.user.views import api, template

urlpatterns = [
    path(
        "verification/<str:username>/<str:token>",
        template.VerificationView.as_view(),
        name="verification",
    ),
    path("login/", api.LoginView.as_view(), name="login"),
    # path('register'),
    # path('logout'),
    # path('forget-password'),
]
