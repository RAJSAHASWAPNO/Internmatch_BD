from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'employer':
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap


def user_is_student(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'student':
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap




class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.role == 'employer'


class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
   
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.role == 'student'