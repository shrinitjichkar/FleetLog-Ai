from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
from inspection.models import Inspection


class IsInspectionOwner(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role not in ['supervisor', 'assessor']:
            return False

        inspection_id = view.kwargs.get('inspection_pk')
        try:
            inspection = Inspection.objects.get(pk=inspection_id)
        except Inspection.DoesNotExist:
            raise NotFound('Inspection not found.')

        view.inspection = inspection

        if request.user.role == 'supervisor':
            return True
        return inspection.assessor_id == request.user.id