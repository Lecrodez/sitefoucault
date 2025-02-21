from django.contrib import admin
from . import models


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UsersAdmin)


class RolesAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Roles, RolesAdmin)
