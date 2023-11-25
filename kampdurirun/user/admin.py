from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User
from user.forms import UserUpdateForm

class UserAdminConfig(UserAdmin):
    model = User
    add_form = UserUpdateForm
    form = UserUpdateForm

    # Customize the fields to display in the admin list view
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_superuser')

    # Add search functionality for email and username
    search_fields = ('email', 'username')

    # Make date_joined and last_login readonly
    readonly_fields = ('date_joined', 'last_login')

    # Customize the sections in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customize the filter options
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Ensure that fields in add form are correctly displayed
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    # Remove the line causing the error
    filter_horizontal = ()

# Register the custom UserAdminConfig with the User model
admin.site.register(User, UserAdminConfig)
