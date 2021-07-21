from django.contrib.auth.models import Group
from modeler.models import AbstractInputDataPoint, Tag, Modeler, ThresholdValue
from modeler.models import GraphCollection, Graph, Node, Weight
from modeler.models import Input, AbstractInputOption
from rest_framework import permissions
from rest_framework_api_key.permissions import BaseHasAPIKey

from .models import OrganizationAPIKey, Organization, User


class HasOrganizationAPIKey(BaseHasAPIKey):
    model = OrganizationAPIKey


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


#### ========================== Permission Classes ============================


class IsIntuitxAdminUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['intuitxadmin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and request.user.is_authenticated and has_group_permission


class IsSuperAdminUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['superadmin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)

        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        has_tenant_access = HasTenantAccess.has_object_permission(self, request, view, obj)

        # disallow any operations on Tenant model objects except Updates on owned tenant
        if isinstance(obj, Organization) and (
                self.action == 'create' or self.action == 'list' or self.action == 'destroy'):
            return False

        if view.action == 'destroy':
            # if Admin is deleting a user; make sure it's not of types IntuitxAdmin or SuperAdmin
            if request.data.get('groups'):
                assigned_groups = request.data.get('groups')
                if any(group.name in ['intuitxadmin'] for group in assigned_groups):
                    return False

        if view.action == 'create':
            # check if the object being created has the right tenant assignment
            if request.user.organization.subdomain_prefix != request.data.get('organization').subdomain_prefix:
                return False
            # if Admin is creating user; make sure it's not of types IntuitxAdmin
            if request.data.get('groups'):
                assigned_groups = request.data.get('groups')
                if any(group.name in ['intuitxadmin'] for group in assigned_groups):
                    return False

        return has_group_permission and has_tenant_access


class IsAdminUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)

        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        has_tenant_access = HasTenantAccess.has_object_permission(self, request, view, obj)
        # disallow any operations on Tenant model objects
        is_interacting_worg = isinstance(obj, Organization)

        if view.action == 'destroy':
            # if Admin is deleting a user; make sure it's not of types IntuitxAdmin or SuperAdmin
            if request.data.get('groups'):
                assigned_groups = request.data.get('groups')
                if any(group.name in ['superadmin', 'intuitxadmin'] for group in assigned_groups):
                    return False

        if view.action == 'create':
            # check if the object being created has the right tenant assignment
            if request.user.organization.subdomain_prefix != request.data.get('organization').subdomain_prefix:
                return False
            # if Admin is creating user; make sure it's not of types IntuitxAdmin or SuperAdmin
            if request.data.get('groups'):
                assigned_groups = request.data.get('groups')
                if any(group.name in ['superadmin', 'intuitxadmin'] for group in assigned_groups):
                    return False

        return has_group_permission and has_tenant_access and not is_interacting_worg


class IsModelerUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['modeler']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)

        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        has_tenant_access = HasTenantAccess.has_object_permission(self, request, view, obj)

        if view.action == 'create':
            # check if the object being created has the right tenant assignment
            if request.user.organization.subdomain_prefix != request.data.get('organization').subdomain_prefix:
                return False

        # disallow any operations on User model objects except Updates on own user
        if isinstance(obj, User) and (self.action == 'create' or self.action == 'list' or self.action == 'destroy'):
            return False
        elif obj != request.user:
            return False

        # disallow any operations on unauthorized data
        if isinstance(obj, Organization) or isinstance(obj, AbstractInputDataPoint) or isinstance(obj,
                                                                                                  Input) or isinstance(
                obj, AbstractInputOption):
            return False

        return has_group_permission and has_tenant_access


class IsDbankerUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['dbanker']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)

        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        has_tenant_access = HasTenantAccess.has_object_permission(self, request, view, obj)

        if view.action == 'create':
            # check if the object being created has the right tenant assignment
            if request.user.organization.subdomain_prefix != request.data.get('organization').subdomain_prefix:
                return False

        # disallow any operations on User model objects except Updates on own user
        if isinstance(obj, User) and (self.action == 'create' or self.action == 'list' or self.action == 'destroy'):
            return False
        elif obj != request.user:
            return False

        # disallow any operations on unauthorized data
        if isinstance(obj, Organization) or isinstance(obj, AbstractInputDataPoint):
            return False

        # disallow operations on Create/Delete/Edit for modelling features
        if (isinstance(obj, GraphCollection) or isinstance(obj, Graph) or isinstance(obj, Modeler) or isinstance(obj,
                                                                                                                 Tag) or isinstance(
                obj, ThresholdValue)) and not (self.action == 'retrieve' or self.action == 'list'):
            return False

        return has_group_permission and has_tenant_access


class IsRegularUserWithAuth(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['reguser']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)

        return request.user and request.user.is_authenticated and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        has_tenant_access = HasTenantAccess.has_object_permission(self, request, view, obj)

        if view.action == 'create':
            # check if the object being created has the right tenant assignment
            if request.user.organization.subdomain_prefix != request.data.get('organization').subdomain_prefix:
                return False

        # disallow any operations on User model objects except Updates on own user
        if isinstance(obj, User) and (self.action == 'create' or self.action == 'list' or self.action == 'destroy'):
            return False
        elif obj != request.user:
            return False

        # disallow any operations on unauthorized data
        if isinstance(obj, Organization):
            return False

        # disallow operations on Create/Delete/Edit for modelling features
        if (isinstance(obj, Input) or isinstance(obj, AbstractInputOption) or isinstance(obj, Graph) or isinstance(obj,
                                                                                                                   GraphCollection) or isinstance(
                obj, Node) or isinstance(obj, Weight) or isinstance(obj, Modeler) or isinstance(obj, Tag) or isinstance(
                obj, ThresholdValue)) and not (self.action == 'retrieve' or self.action == 'list'):
            return False

        return has_group_permission and has_tenant_access


class HasTenantAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.organization == request.user.organization


class HasGuestTenantAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return any([obj.organization == g_org for g_org in request.user.guest_organizations])
