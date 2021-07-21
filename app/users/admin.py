from admin_helpers import AdminChangeLinksMixin
from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from rest_framework_api_key.admin import APIKeyModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import OrganizationAPIKey
# from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Company


@admin.register(OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = [*APIKeyModelAdmin.list_display, "organization"]
    search_fields = [*APIKeyModelAdmin.search_fields, "organization"]


class BaseModelAdmin(admin.ModelAdmin):

    def has_view_permission(self, request, obj=None):

        opts = self.opts
        codename_view = get_permission_codename('view', opts)
        codename_change = get_permission_codename('change', opts)
        base_perm = request.user.has_perm('%s.%s' % (opts.app_label, codename_view)) or request.user.has_perm(
            '%s.%s' % (opts.app_label, codename_change))

        try:
            # company_permission = obj.company==request.user.company
            companies_list = []
            for co in request.user.companies.all():
                companies_list.append(co.id)
            if base_perm and obj.companies.filter(id__in=request.user.companies.all()).exists():
                True
        except AttributeError:
            if base_perm:
                return True
        return False

    '''
    def has_add_permission(request):
        pass

    def has_change_permission(request , obj):
        pass

    def has_delete_permission(request , obj):
        pass

    def has_module_permission(request):
        pass
    '''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(companies__in=request.user.companies.all())
        # return qs.filter(company=request.user.company)


class CompanyAdmin(AdminChangeLinksMixin, BaseModelAdmin):
    list_display = ('name', 'project_companies_link',)
    changelist_links = ('project_companies', 'company_strategies', 'company_products')
    search_fields = ('name',)


'''
class UserAdmin(AdminChangeLinksMixin, UserAdmin):
    list_display = ('name', 'email', 'date_joined', 'is_active')
    list_filter = ('is_active',)
    filter_horizontal = ('groups', 'guest_organizations')
    #change_links = ('organization',)
    search_fields = ('name', 'email')
'''


class CustomUserAdmin(UserAdmin, BaseModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('name', 'email', 'date_joined', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    filter_horizontal = ('groups', 'guest_organizations')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Groups', {'fields': ('groups',)}),
        ('Organizations', {'fields': ('organizations', 'guest_organizations', 'companies')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'name', 'email', 'password1', 'password2', 'is_staff', 'is_admin', 'is_superuser', 'is_active', 'groups',
            'organizations', 'companies', 'guest_organizations')}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Organization)
