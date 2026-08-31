from rest_framework.permissions import BasePermission


from rest_framework.permissions import BasePermission


class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'renter')


class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'supervisor')


class IsAssessor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'assessor')


class IsRenterOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in ['renter', 'supervisor']
        )


class IsSupervisorOrAssessor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in ['supervisor', 'assessor']
        )
    
    
class IsAssignedAssessorOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in ['supervisor', 'assessor']
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'supervisor':
            return True
        return obj.assessor_id == request.user.id