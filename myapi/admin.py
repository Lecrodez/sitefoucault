from django.contrib import admin
from . import models


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UsersAdmin)


class RolesAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Roles, RolesAdmin)


class SurveyAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Survey, SurveyAdmin)


class QuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Question, QuestionAdmin)


class QuestionTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.QuestionType, QuestionTypeAdmin)


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Answer, AnswerAdmin)


class AnswerTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.AnswerType, AnswerTypeAdmin)
