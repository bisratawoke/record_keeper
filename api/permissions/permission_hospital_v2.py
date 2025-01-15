from rest_framework.permissions import BasePermission
from ..models import Hospital
class PermissionHospitalV2(BasePermission):

    def has_permission(self,request):
        if not request.user:
            return False
        return True

    def has_object_permission(self,request,view,obj):
        hospital_id = view.kwargs.get('id')
        hospital = Hospital.objects.get(hospital_id)

        if request.user != hospital.owner:
            return False
        return True



