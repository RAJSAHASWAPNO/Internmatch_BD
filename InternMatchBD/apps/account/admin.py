from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
    User,
    EmployeeProfile,
    EmployerProfile,
    EmployeeEducation,
    EmployeeExperience,
    EmployeeCertification,
    EmployeeProject,
)


class AddUserForm(forms.ModelForm):
   
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'role', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'gender', 'role', 'last_name', 'is_active',
            'is_staff'
        )

    def clean_password(self):

        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email', 'first_name', 'last_name', 'gender', 'role', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'role', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'gender', 'role', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

class EmployeeEducationInline(admin.TabularInline):
    model = EmployeeEducation
    extra = 1
    fields = ['degree', 'field_of_study', 'institution', 'start_date', 'end_date', 'is_current']


class EmployeeExperienceInline(admin.TabularInline):
    model = EmployeeExperience
    extra = 1
    fields = ['job_title', 'company', 'start_date', 'end_date', 'is_current']


class EmployeeCertificationInline(admin.TabularInline):
    model = EmployeeCertification
    extra = 1
    fields = ['title', 'issuer', 'issue_date', 'expiry_date', 'credential_url']


class EmployeeProjectInline(admin.TabularInline):
    model = EmployeeProject
    extra = 1
    fields = ['title', 'url', 'technologies']


# Employee Profile Admin
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_email', 'get_user_name', 'phone_number', 'location', 'availability_status']
    list_filter = ['availability_status', 'user']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone_number', 'location']
    readonly_fields = ['created_at'] if hasattr(EmployeeProfile, 'created_at') else []
    inlines = [
        EmployeeEducationInline,
        EmployeeExperienceInline,
        EmployeeCertificationInline,
        EmployeeProjectInline,
    ]
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'location')
        }),
        ('Professional Information', {
            'fields': ('bio', 'resume', 'availability_status', 'languages', 'skills')
        }),
        ('Social Links', {
            'fields': ('social_linkedin', 'social_github')
        }),
    )
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'Name'


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(EmployerProfile)

@admin.register(EmployeeEducation)
class EmployeeEducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field_of_study', 'institution', 'get_employee_email', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['institution', 'employee__user__email', 'degree', 'field_of_study']
    
    def get_employee_email(self, obj):
        return obj.employee.user.email
    get_employee_email.short_description = 'Employee'


@admin.register(EmployeeExperience)
class EmployeeExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'get_employee_email', 'start_date', 'is_current']
    list_filter = ['is_current', 'company', 'start_date']
    search_fields = ['job_title', 'company', 'employee__user__email']
    
    def get_employee_email(self, obj):
        return obj.employee.user.email
    get_employee_email.short_description = 'Employee'


@admin.register(EmployeeCertification)
class EmployeeCertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'get_employee_email', 'issue_date', 'expiry_date']
    list_filter = ['issue_date', 'issuer']
    search_fields = ['title', 'issuer', 'employee__user__email']
    
    def get_employee_email(self, obj):
        return obj.employee.user.email
    get_employee_email.short_description = 'Employee'


@admin.register(EmployeeProject)
class EmployeeProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_employee_email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'employee__user__email', 'technologies']
    
    def get_employee_email(self, obj):
        return obj.employee.user.email
    get_employee_email.short_description = 'Employee'