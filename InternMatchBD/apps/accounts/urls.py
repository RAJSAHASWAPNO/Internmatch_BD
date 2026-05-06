from django.urls import path
from account.views import (
    StudentEditProfileView,
    EmployerEditProfileView,
    StudentRegistrationView,
    EmployerRegistrationView,
    UserLoginView,
    UserLogoutView,
    CandidateProfileView,
    EmployerProfileView,
)

app_name = "account"

urlpatterns = [
    path('student/register/', StudentRegistrationView.as_view(), name='student-registration'),
    path('employer/register/', EmployerRegistrationView.as_view(), name='employer-registration'),
    path('profile/edit/<int:id>/', StudentEditProfileView.as_view(), name='edit-profile'),
    path('employer/profile/edit/<int:id>/', EmployerEditProfileView.as_view(), name='employer-edit-profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('candidate/profile/<int:id>/', CandidateProfileView.as_view(), name='candidate-profile'),
    path('employer/profile/view/<int:id>/', EmployerProfileView.as_view(), name='employer-profile'),
]