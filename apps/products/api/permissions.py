from rest_framework import permissions


class IsOwnerCart(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.customer == request.user


class IsOwnerCartItem(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.cart.customer == request.user


class IsOwnerOrder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.customer == request.user
