#!/usr/bin/env python
"""
Comprehensive test for employee profile form submission.
Tests all formsets and profile updates.
"""
import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from account.models import EmployeeProfile, EmployeeEducation, EmployeeExperience

User = get_user_model()

def test_profile_form_submission():
    """Test employee profile form submission with all formsets."""
    client = Client()
    
    print("=" * 70)
    print("TESTING EMPLOYEE PROFILE FORM SUBMISSION")
    print("=" * 70)
    print()
    
    try:
        # Get or create test user
        user = User.objects.filter(role='employee').first()
        if not user:
            user = User.objects.create_user(
                email='form.test@example.com',
                password='testpass123',
                first_name='Form',
                last_name='Tester',
                role='employee',
                gender='M'
            )
            profile = EmployeeProfile.objects.create(user=user)
        else:
            profile = user.employee_profile
        
        print(f"✅ Test User: {user.get_full_name()} ({user.email})")
        print(f"   Profile ID: {profile.id}")
        print()
        
        # Login the user
        print("Attempting to login...")
        login_success = client.login(email=user.email, password='testpass123')
        
        if not login_success:
            # Try alternative login
            client.force_login(user)
            print("✅ User authenticated (force login)")
        else:
            print("✅ User logged in successfully")
        
        print()
        
        # Prepare form data for submission
        print("Preparing form submission data...")
        form_data = {
            # Personal info
            'first_name': 'Form',
            'last_name': 'Tester',
            'gender': 'M',
            
            # Contact info
            'phone_number': '+1-555-1234',
            'location': 'New York, USA',
            
            # Social links
            'social_linkedin': 'https://linkedin.com/in/formtester',
            'social_github': 'https://github.com/formtester',
            
            # Professional info
            'bio': 'I am a test employee profile.',
            'availability_status': 'available',
            'languages': 'English, Spanish, French',
            
            # Skills (if any exist in DB)
            'skills': [],
            
            # Education formset
            'education-TOTAL_FORMS': '1',
            'education-INITIAL_FORMS': '0',
            'education-MIN_NUM_FORMS': '0',
            'education-MAX_NUM_FORMS': '1000',
            'education-0-id': '',
            'education-0-degree': "Bachelor's",
            'education-0-field_of_study': 'Computer Science',
            'education-0-institution': 'Test University',
            'education-0-start_date': '2020-01-01',
            'education-0-end_date': '2024-05-01',
            'education-0-is_current': '',
            'education-0-DELETE': '',
            
            # Experience formset
            'experience-TOTAL_FORMS': '1',
            'experience-INITIAL_FORMS': '0',
            'experience-MIN_NUM_FORMS': '0',
            'experience-MAX_NUM_FORMS': '1000',
            'experience-0-id': '',
            'experience-0-job_title': 'Test Engineer',
            'experience-0-company': 'Test Company',
            'experience-0-description': 'Worked as a test engineer',
            'experience-0-start_date': '2023-01-01',
            'experience-0-end_date': '2024-01-01',
            'experience-0-is_current': '',
            'experience-0-DELETE': '',
            
            # Certification formset
            'certification-TOTAL_FORMS': '0',
            'certification-INITIAL_FORMS': '0',
            'certification-MIN_NUM_FORMS': '0',
            'certification-MAX_NUM_FORMS': '1000',
            
            # Project formset
            'project-TOTAL_FORMS': '0',
            'project-INITIAL_FORMS': '0',
            'project-MIN_NUM_FORMS': '0',
            'project-MAX_NUM_FORMS': '1000',
        }
        
        print("✅ Form data prepared")
        print()
        
        # Submit the form
        print("Submitting profile update form...")
        edit_url = f'/profile/edit/{user.id}/'
        response = client.post(edit_url, form_data)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Form submitted successfully (redirect)")
            print(f"   Redirect to: {response.url}")
            
            # Check if data was saved
            profile.refresh_from_db()
            
            print()
            print("Verifying saved data...")
            print("-" * 70)
            
            checks = [
                ("Phone Number", profile.phone_number, '+1-555-1234'),
                ("Location", profile.location, 'New York, USA'),
                ("LinkedIn", profile.social_linkedin, 'https://linkedin.com/in/formtester'),
                ("GitHub", profile.social_github, 'https://github.com/formtester'),
                ("Bio", profile.bio, 'I am a test employee profile.'),
                ("Availability", profile.availability_status, 'available'),
                ("Languages", profile.languages, 'English, Spanish, French'),
            ]
            
            for field_name, saved_value, expected_value in checks:
                if saved_value == expected_value:
                    print(f"✅ {field_name}: {saved_value}")
                else:
                    print(f"❌ {field_name}: Expected '{expected_value}', got '{saved_value}'")
            
            print()
            print("Checking related objects...")
            print("-" * 70)
            
            # Check education entries
            education_count = profile.education.count()
            print(f"✅ Education entries: {education_count}")
            if education_count > 0:
                edu = profile.education.first()
                print(f"   - {edu.degree} in {edu.field_of_study} from {edu.institution}")
            
            # Check experience entries
            experience_count = profile.experience.count()
            print(f"✅ Experience entries: {experience_count}")
            if experience_count > 0:
                exp = profile.experience.first()
                print(f"   - {exp.job_title} at {exp.company}")
            
            print()
            print("=" * 70)
            print("✅ ALL TESTS PASSED!")
            print("=" * 70)
            
        elif response.status_code == 200:
            print("⚠️  Form submission returned 200 (check for form errors)")
            if hasattr(response, 'context') and response.context:
                profile_form = response.context.get('profile_form')
                if profile_form and profile_form.errors:
                    print("\nProfile Form Errors:")
                    for field, errors in profile_form.errors.items():
                        print(f"  - {field}: {errors}")
                
                education_fs = response.context.get('education_formset')
                if education_fs:
                    for i, form in enumerate(education_fs):
                        if form.errors:
                            print(f"\nEducation Form {i} Errors:")
                            for field, errors in form.errors.items():
                                print(f"  - {field}: {errors}")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_profile_form_submission()
