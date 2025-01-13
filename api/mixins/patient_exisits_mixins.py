from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Patient

class PatientExistsMixins:
    def check_patient_exists(self, id):
        if not Patient.objects.filter(id=id).exists():
            raise NotFound(detail="Patient not found")