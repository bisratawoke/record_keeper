from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Doctor,Patient ,PatientHistory
from .serializers import DoctorSerialzier,PatientSerializer,CreatePatienSerialzier,PatientHistorySerializer
from .mixins.patient_exisits_mixins import PatientExistsMixins
from .dto.create_patient_dto import CreatePatientDto
from .dto.create_patient_history_dto import CreatePatientHistoryDto
from .dto.update_patient_history_dto import UpdatePatientHistoryDto
from .dto.delete_patient_history_dto import DeletePatientHistoryDto

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
        

