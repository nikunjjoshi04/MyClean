from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeamMembers

# Register your models here.


# class UserAdmin(admin.ModelAdmin):
UserAdmin.fieldsets += ('Custom fields set', {'fields': ('user_type',)}),
UserAdmin.list_display += ('user_type',)


admin.site.register(User, UserAdmin)
admin.site.register(TeamMembers)