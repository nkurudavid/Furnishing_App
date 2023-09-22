from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'is_superuser','is_manager','is_craftsman','is_client','is_active','last_login',)
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_client', 'is_manager', 'is_superuser', 'is_active')
    fieldsets = (
        ('User Credential', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender',)}),
        ('Permissions', {'fields': (('is_manager','is_client'),('is_active', 'is_staff', 'is_superuser'), 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('New User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'gender',),
        }),
        ('User Credential', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
        ('Permission', {
            'classes': ('whide',),
            'fields': (('is_manager','is_client','is_craftsman'),('is_active', 'is_superuser'),),
        }),
    )
    ordering = ('email',)
    list_editable = ()
    list_per_page = 20



@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('client', 'phone_number', 'location', 'shipping_location', 'shipping_street',)
    search_fields = ('client', 'phone_number',)
    fieldsets = (
        ('User Profile', {'fields': ('client', 'phone_number', 'location', 'shipping_location', 'shipping_street',)}),
    )
    add_fieldsets = (
        ('New Profile', {
            'classes': ('wide',),
            'fields': ('client', 'phone_number', 'location', 'shipping_location', 'shipping_street',),
        }),
    )
    ordering = ('client',)
    list_editable = ()
    list_per_page = 20



admin.site.unregister(Group)
