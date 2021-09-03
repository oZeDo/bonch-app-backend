from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user.id)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


def deactivate_selected(UserAdmin, request, queryset):
    rows_updated = queryset.update(is_staff=0)
    for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 запись была успешно деактивирована.'
    else:
        message_bit = '%s были деактивированы ' % rows_updated
    UserAdmin.message_user(request, message_bit)


deactivate_selected.short_description = "Деактивировать выделенные записи"

# add deactivates
admin.site.add_action(deactivate_selected)


def activate_selected(UserAdmin, request, queryset):
    rows_updated = queryset.update(is_staff=1)
    for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 запись была успешно активирована.'
    else:
        message_bit = '%s были активированы ' % rows_updated
    UserAdmin.message_user(request, message_bit)


activate_selected.short_description = "Активировать выделенные записи"

# add deactivates
admin.site.add_action(activate_selected)

