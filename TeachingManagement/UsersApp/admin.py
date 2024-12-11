from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Professor,Chief,ProfessorField,ProfessorLanguage

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # include it in the add form
    )
    list_display = UserAdmin.list_display + ('role',)


admin.site.register(CustomUser, CustomUserAdmin)

class ProfessorAdmin(admin.ModelAdmin):
    list_display=["idProfessor","user","name","family_name","description","comment","email","isActive"]
    list_filter=("isActive",)

admin.site.register(Professor, ProfessorAdmin)

class CheifAdmin(admin.ModelAdmin):
    list_display=["professor","section"]

admin.site.register(Chief, CheifAdmin)

class ProfessorFieldAdmin(admin.ModelAdmin):
    list_display=["idProfessorField","Professor","Field"]

admin.site.register(ProfessorField,ProfessorFieldAdmin)

class ProfessorLanguageAdmin(admin.ModelAdmin):
    list_display=["idProfessorLanguage","Professor","Language"]

admin.site.register(ProfessorLanguage,ProfessorLanguageAdmin)
