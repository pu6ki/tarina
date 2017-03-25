from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author.user


class IsNotBlacklisted(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user not in obj.blacklist.all()
