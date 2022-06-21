from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'bio',
        'email',
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
