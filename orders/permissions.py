from rest_framework.permissions import  BasePermission

class IsStafforReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return (
                request.user.is_authenticated and request.user.is_staff
            )
        return True


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.customer == request.user