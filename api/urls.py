from django.urls import path
from .views import DoctorCrudView

urlpatterns = [
    path('doctor/',DoctorCrudView.as_view())
]
