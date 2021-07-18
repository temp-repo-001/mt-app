from django.contrib import admin

# Register your models here.
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
    ]
    list_display_links = [
        "id",
        "username",
        "email",
    ]
    search_fields = [
        "id",
        "username",
        "email",
    ]
    exclude = ["id"]
