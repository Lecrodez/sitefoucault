from django.contrib import admin
from users import models


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)


class RolesAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Roles, RolesAdmin)
