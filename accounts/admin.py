from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = ("email",)
    fieldsets = (
        (
            None,
            {"fields": ("username", "first_name", "last_name", "email", "password")},
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if change:
            if "password" in form.changed_data:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
