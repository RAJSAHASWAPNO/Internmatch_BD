from django import forms
from account.models import User, StudentProfile, EmployerProfile

class StudentProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["resume", "bio", "skills"]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ["company_website", "company_logo", "description"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your company...'}),
        }