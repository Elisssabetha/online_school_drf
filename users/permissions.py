from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name="Moderator").exists() and request.method not in ['POST', 'DELETE']
