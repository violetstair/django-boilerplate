from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request._auth['user_id'] == view.kwargs['pk']:
            return True
        else:
            print('*' * 55)
            print(request._auth['user_id'], ' == ', view.kwargs['pk'])
            print('*' * 55)
            return False

    def has_object_permission(self, request, view, obj):
        return obj == request.user
