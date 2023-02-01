from rest_framework import permissions


class DjangoRoleBasedPermission(permissions.BasePermission):
    perms_map = {
        'OPTION-LIST': ['Admin','Case Study Editor', 'Case Study Manager',],
        'GET': ['Admin','Case Study Editor', 'Case Study Manager','Viewer'],
        'OPTIONS': [],
        'HEAD': [],
        # 'POST': ['Admin','Case Study Editor', 'Case Study Manager',],
        # 'PUT': ['Admin','Case Study Editor', 'Case Study Manager',],
        # 'PATCH': ['Admin','Case Study Editor', 'Case Study Manager',],
        # 'DELETE': ['Admin','Case Study Editor', 'Case Study Manager',],
        'POST': ['Admin',],
        'PUT': ['Admin',],
        'PATCH': ['Admin',],
        'DELETE': ['Admin',],
    }

    def isOwner(self, request, obj):
        if hasattr(obj, 'owner') and hasattr(obj.owner, 'id') and obj.owner.id == request.user.id:
            return True
        return False

    def has_permission(self, request, view):
        # print("has_permission")
        ## CHECK FOR OPTION LIST
        if request.resolver_match.url_name.find('-option-list') > -1:
            self.perms_map['GET'] = self.perms_map['OPTION-LIST']
        if not hasattr(request.user, 'has_admin_group'):
            return False
        if hasattr(request.user, 'has_admin_group') and request.user.has_admin_group is True:
            return True
        return request.user.has_group(self.perms_map.get(request.method))


    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'has_admin_group') and request.user.has_admin_group is True:
            return True
        if self.isOwner(request, obj):
            # print("isOwner")
            return True
        if not hasattr(obj, 'users'):
            return True
        if request.user in obj.users.all():
            # print("has_user")
            return True
        return False


class DjangoAdminOrObjectPermission(permissions.DjangoObjectPermissions):

    perms_map = {
        'OPTION-LIST': ['%(app_label)s.option_list_%(model_name)s'],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_admin_group(self, request):
        if hasattr(request.user, 'has_admin_group') and request.user.has_admin_group is True:
            return True

    def has_permission(self, request, view):
        ## CHECK FOR OPTION LIST
        if request.resolver_match.url_name.find('-option-list') > -1:
            self.perms_map['GET'] = self.perms_map['OPTION-LIST']

        if self.has_admin_group(request):
            return True

        return super(DjangoAdminOrObjectPermission, self).has_permission(request, view)


    def has_object_permission(self, request, view, obj):
        # print("has_object_permission")
        if self.has_admin_group(request):
            return True
        return super(DjangoAdminOrObjectPermission, self).has_object_permission(request, view, obj)


class DjangoOwnerOrAdminOrObjectPermission(DjangoAdminOrObjectPermission):
    def isOwner(self, request, obj):
        if hasattr(obj, 'owner') and hasattr(obj.owner, 'id') and obj.owner.id == request.user.id:
            # print("isOwner")
            return True
        # print("NOT isOwner")
        return False

    def has_object_permission(self, request, view, obj):
        # print("has_object_permission")
        if self.has_admin_group(request) or self.isOwner(request, obj) is True:
            return True
        return super(DjangoAdminOrObjectPermission, self).has_object_permission(request, view, obj)
