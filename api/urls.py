from django.urls import path
from .views import DoctorCrudView,PatientCrudView,PatientHistoryCrudView,HospitalCrudView

urlpatterns = [
    path('doctor/',DoctorCrudView.as_view()),
    path('patient/',PatientCrudView.as_view()),
    path('patient/<int:id>/history',PatientHistoryCrudView.as_view()),
    path('hosptial/',HospitalCrudView.as_view())
]
