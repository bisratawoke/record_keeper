from django.urls import path
from .views import (
    DoctorCrudView,
    PatientCrudView,
    PatientHistoryCrudView,
    HospitalCrudView,
    AssetCategoryCrudView
)
urlpatterns = [
    path('doctor/',DoctorCrudView.as_view()),
    path('patient/',PatientCrudView.as_view()),
    path('patient/<int:id>/history',PatientHistoryCrudView.as_view()),
    path('hospital/',HospitalCrudView.as_view()),
    path('hospital/<int:id>/asset-category',AssetCategoryCrudView.as_view())
]
