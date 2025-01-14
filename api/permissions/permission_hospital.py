from rest_framework.permissions import BasePermission
from ..dto.update_hospital_dto import UpdateHospitalDto


class HospitalPermission(BasePermission):
    def has_permission(self,request,view):
        if request.user:
            return True
        return False   

    def has_object_permission(self, request, view, obj):   
        if hasattr(obj,"owner") and obj.owner.id == request.user.id:
            return True
        return False