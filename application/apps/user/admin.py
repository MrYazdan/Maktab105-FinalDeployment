from django.contrib import admin
from apps.user.models import User

admin.site.register(
    User,
    readonly_fields=[
        "last_login",
        "date_joined",
        "is_active",
        "is_deleted",
        "is_staff",
        "is_superuser",
    ],
    list_display=["id", "username", "email", "is_active", "last_login", "date_joined"],
)
