from django.urls import path
from .views import DoctorCrudView,PatientCrudView

urlpatterns = [
    path('doctor/',DoctorCrudView.as_view()),
    path('patient/',PatientCrudView.as_view())
]
