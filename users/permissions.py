from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request._auth != None and 'pk' in view.kwargs:
            return request._auth['user_id'] == view.kwargs['pk']
        return False

    def has_object_permission(self, request, view, obj):
        return obj == request.user
