from django.contrib import admin
from .models import Post, Comment, Like

admin.site.register(
    Post,
    readonly_fields=["modify_at", "create_at", "author", "is_active", "is_deleted"],
    list_display=["id", "title", "author", "is_active"],
)

admin.site.register((Comment, Like))
