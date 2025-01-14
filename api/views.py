from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Doctor,Patient ,PatientHistory,Hospital
from .serializers import DoctorSerialzier,PatientSerializer,CreatePatienSerialzier,PatientHistorySerializer,HospitalSerializer
from .mixins.patient_exisits_mixins import PatientExistsMixins
from .mixins.record_exisits_mixins import RecordExisitsMixin
from .dto.create_patient_dto import CreatePatientDto
from .dto.create_patient_history_dto import CreatePatientHistoryDto
from .dto.update_patient_history_dto import UpdatePatientHistoryDto
from .dto.delete_patient_history_dto import DeletePatientHistoryDto
from .dto.create_hospital_dto import CreateHospitalDto
from.permissions.permission_hospital import HospitalPermission
from rest_framework.exceptions import PermissionDenied

class DoctorCrudView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):
        doctors = Doctor.objects.select_related("user")
        result = DoctorSerialzier(doctors,many=True)
        return Response(data={'data':result.data})
    def post(self,request):
        data = request.data
        serializer = DoctorSerialzier(data={**data,'user':request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message':'Doctor created successfully'})
        else:
            return Response(data={'message':serializer.errors})
        


class PatientCrudView(APIView):
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        patients = Patient.objects.select_related("user")
        data = PatientSerializer(patients,many=True).data
        return Response(data={
            'data': data
        })

    def post(self,request):
        body = request.data
        dto = CreatePatientDto(data=body)
        if not dto.is_valid():
            return Response(data={'message':dto.errors})
        serialzier = CreatePatienSerialzier(data={'name':dto.validated_data['name'],'primary_doctor':dto.validated_data['doctor'],'user':request.user.id})

        if serialzier.is_valid():
            serialzier.save()
            return Response(data={'message':'Patient created successfully'})
        return Response(data={'message':serialzier.errors})

    def put(self,request):
        body = request.data
        patient = Patient.objects.get(id=body['id'])
        serialzier = CreatePatienSerialzier(patient,data=body,partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(data={'message':'Patient updated successfully'})
        return Response(data={'message':serialzier.errors})

    def delete(self,request):
        body = request.data
        try:
            patient = Patient.objects.get(id=body['id'])
        except Patient.DoesNotExist:
            return Response(data={'message':'Patient does not exist'})
        patient.delete()
        return Response(data={'message':'Patient deleted successfully'})
    


class PatientHistoryCrudView(APIView,PatientExistsMixins):

    def get(self,request,id):
        self.check_patient_exists(id)
        history = PatientHistory.objects.filter(patient=id)
        data = PatientHistorySerializer(history,many=True).data
        return Response(data={'data':data})
    
    def post(self,request,id):
        self.check_patient_exists(id)
        body = CreatePatientHistoryDto(data=request.data)
        if not body.is_valid():
            return Response(data={'message':body.errors})
        history = PatientHistorySerializer(data={'patient':id,'description':body.validated_data['description']})
        if not history.is_valid():
            return Response(data={'message':history.errors})
        history.save()
        return Response(data={'message':'History created successfully'})
    
    def patch(self,request,id):
        self.check_patient_exists(id)
        body = UpdatePatientHistoryDto(data=request.data)
        if not body.is_valid():
            return Response(data={'message':body.errors})
        history = PatientHistory.objects.update(**body.validated_data)
        return Response(data={'message':'History updated successfully'})
    
    def delete(self,request,id):
        self.check_patient_exists(id)
        body = DeletePatientHistoryDto(data=request.data)

        if not body.is_valid():
            return Response(data={'message':body.errors})

        res = PatientHistory.objects.get(**body.validated_data)
        res.delete()
        return Response(data={'message':'History deleted successfully'})        
        



class HospitalCrudView(APIView,RecordExisitsMixin):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated & HospitalPermission]
    def get(self,request):
        hospitals = Hospital.objects.all()
        data = HospitalSerializer(hospitals,many=True).data
        return Response(data={'data':data})
        

    def post(self,request):
        body = CreateHospitalDto(data=request.data)
        if not body.is_valid():
            return Response(status=400,data={'message': body.errors})
        hospital = HospitalSerializer(data=body.validated_data)
        if not hospital.is_valid():
            return Response(status=400,data={'message':hospital.errors})
        hospital.save()
        return Response({
            'message':'Hospital created successfully'
        })
    
    def patch(self,request):
        self.check_if_record_exisits(Hospital,request.data['id'])
        body = request.data
        hospital = Hospital.objects.get(id=body['id'])
        try:
            self.check_object_permissions(request=request,obj=hospital)
        except PermissionDenied:
            return Response(data={'message':'Permission denined'})
   
        serializer = HospitalSerializer(hospital,data=body,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message':'Hospital updated successfully'})
        return Response(data={'message':serializer.errors})

    
    def delete(self,request):
        self.check_if_record_exisits(Hospital,request.data['id'])
        body = request.data
        hospital = Hospital.objects.get(id=body['id'])
        hospital.delete()
        return Response(data={'message':'Hospital deleted successfully'})