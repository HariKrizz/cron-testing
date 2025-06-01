from . import views
from django.urls import path


app_name = 'students'


urlpatterns = [
    path('create-student/', views.CreateStudentView.as_view(), name='create_student'),

]