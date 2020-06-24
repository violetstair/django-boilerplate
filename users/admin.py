from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'created_at',
        'updated_at',
    )

    list_display_links = (
        'id',
        'username',
        'email',
    )


admin.site.unregister(Group)
