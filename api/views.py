from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Doctor,Patient
from .serializers import DoctorSerialzier,PatientSerializer,CreatePatienSerialzier


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

        serialzier = CreatePatienSerialzier(data={**body,'primary_doctor':body['doctor'],'user':request.user.id})

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
    