from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('university_email', 'full_name', 'father_name', 'department', "whatsapp_number", 'university_roll_no', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'department')
    search_fields = ('university_email', 'full_name', 'university_roll_no', "whatsapp_number")
    ordering = ('university_email',)

    fieldsets = (
        (None, {'fields': ('university_email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'father_name', 'department', 'whatsapp_number', 'university_roll_no')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('university_email', 'full_name', 'father_name', 'department','whatsapp_number', 'university_roll_no', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
