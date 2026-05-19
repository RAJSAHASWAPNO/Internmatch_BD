from django import forms
from account.models import (
    User, EmployeeProfile, EmployerProfile,
    EmployeeEducation, EmployeeExperience, EmployeeCertification, EmployeeProject,
    AVAILABILITY_STATUS_CHOICES
)
from jobapp.models import Skill

class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]

class EmployerUserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployerUserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class EmployeeProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = EmployeeProfile
        fields = ["resume", "bio", "phone_number", "location", "availability_status", "languages", "social_linkedin", "social_github", "skills"]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+1 (555) 000-0000', 'type': 'tel'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'availability_status': forms.Select(attrs={'class': 'form-control'}),
            'languages': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g., English, French, Spanish\n(separated by commas or newlines)'}),
            'social_linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'social_github': forms.URLInput(attrs={'placeholder': 'https://github.com/yourprofile'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ["company_website", "company_logo", "description"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your company...'}),
        }

# Education Forms
class EmployeeEducationForm(forms.ModelForm):
    class Meta:
        model = EmployeeEducation
        fields = ['degree', 'field_of_study', 'institution', 'start_date', 'end_date', 'is_current']
        widgets = {
            'degree': forms.TextInput(attrs={'placeholder': "e.g., Bachelor's, Master's, PhD"}),
            'field_of_study': forms.TextInput(attrs={'placeholder': 'e.g., Computer Science, Business Administration'}),
            'institution': forms.TextInput(attrs={'placeholder': 'University name'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmployeeEducationFormSet(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        for form in self.forms:
            if form.cleaned_data.get('is_current') and form.cleaned_data.get('end_date'):
                raise forms.ValidationError("Current education shouldn't have an end date.")

EducationFormSet = forms.modelformset_factory(
    EmployeeEducation,
    form=EmployeeEducationForm,
    formset=EmployeeEducationFormSet,
    extra=1,
    can_delete=True
)

# Experience Forms
class EmployeeExperienceForm(forms.ModelForm):
    class Meta:
        model = EmployeeExperience
        fields = ['job_title', 'company', 'description', 'start_date', 'end_date', 'is_current']
        widgets = {
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g., Senior Software Engineer'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your responsibilities and achievements...'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmployeeExperienceFormSet(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        for form in self.forms:
            if form.cleaned_data.get('is_current') and form.cleaned_data.get('end_date'):
                raise forms.ValidationError("Current position shouldn't have an end date.")

ExperienceFormSet = forms.modelformset_factory(
    EmployeeExperience,
    form=EmployeeExperienceForm,
    formset=EmployeeExperienceFormSet,
    extra=1,
    can_delete=True
)

# Certification Forms
class EmployeeCertificationForm(forms.ModelForm):
    class Meta:
        model = EmployeeCertification
        fields = ['title', 'issuer', 'issue_date', 'expiry_date', 'credential_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., AWS Solutions Architect'}),
            'issuer': forms.TextInput(attrs={'placeholder': 'e.g., Amazon Web Services'}),
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'credential_url': forms.URLInput(attrs={'placeholder': 'Link to credential (optional)'}),
        }

CertificationFormSet = forms.modelformset_factory(
    EmployeeCertification,
    form=EmployeeCertificationForm,
    extra=1,
    can_delete=True
)

# Project Forms
class EmployeeProjectForm(forms.ModelForm):
    class Meta:
        model = EmployeeProject
        fields = ['title', 'description', 'url', 'technologies']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your project...'}),
            'url': forms.URLInput(attrs={'placeholder': 'Link to project or repository'}),
            'technologies': forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, React (comma-separated)'}),
        }

ProjectFormSet = forms.modelformset_factory(
    EmployeeProject,
    form=EmployeeProjectForm,
    extra=1,
    can_delete=True
)

