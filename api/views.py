from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Doctor,Patient
from .serializers import DoctorSerialzier,PatientSerializer


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
    
    def get(self,request):
        patients = Patient.objects.select_related("user")
        data = PatientSerializer(patients,many=True)
        return Response({
            'data': {
                'data': data
            }
        })

    def post(self,request):
        body = request.data
        serialzier = PatientSerializer(data={**body,'user':request.user.id})

        if serialzier.is_valid():
            serialzier.save()
            return Response(data={'message':'Patient created successfully'})
        
        return Response(data={'message':serialzier.errors})