from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE'] and request.user.groups.filter(name="Moderator").exists():
            return False
        return True
