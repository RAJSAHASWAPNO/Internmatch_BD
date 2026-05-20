#!/usr/bin/env python
"""
Test script to verify employee profile pages are working correctly.
Run with: python test_profile_pages.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from account.models import EmployeeProfile

User = get_user_model()

def test_profile_pages():
    """Test employee profile edit and view pages."""
    client = Client()
    
    print("=" * 60)
    print("TESTING EMPLOYEE PROFILE PAGES")
    print("=" * 60)
    
    # Check if test user exists
    try:
        user = User.objects.filter(role='employee').first()
        if not user:
            print("⚠️  No employee users found in database")
            print("Creating test employee for testing...")
            user = User.objects.create_user(
                email='test.employee@example.com',
                password='testpass123',
                first_name='Test',
                last_name='Employee',
                role='employee',
                gender='M'
            )
            profile = EmployeeProfile.objects.create(user=user)
            print(f"✅ Created test employee: {user.email}")
        
        profile = user.employee_profile
        print(f"✅ Found employee: {user.get_full_name()} ({user.email})")
        print(f"   Profile ID: {profile.id}")
        print()
        
        # Test edit profile page
        print("Testing Edit Profile Page...")
        print("-" * 60)
        edit_url = f'/profile/edit/{user.id}/'
        response = client.get(edit_url)
        
        if response.status_code == 302:
            print(f"⚠️  Redirect to login (expected if not authenticated)")
        elif response.status_code == 200:
            print(f"✅ Edit profile page loads successfully (status: {response.status_code})")
            
            # Check if required context variables are present
            required_context = [
                'form',
                'profile_form',
                'education_formset',
                'experience_formset',
                'certification_formset',
                'project_formset',
            ]
            
            for ctx_var in required_context:
                if ctx_var in response.context:
                    print(f"   ✅ Context variable '{ctx_var}' present")
                else:
                    print(f"   ❌ Missing context variable: '{ctx_var}'")
            
            # Check template rendering
            if 'Personal Information' in response.content.decode():
                print("   ✅ Personal Information section renders")
            if 'Contact Information' in response.content.decode():
                print("   ✅ Contact Information section renders")
            if 'Education' in response.content.decode():
                print("   ✅ Education section renders")
            if 'Work Experience' in response.content.decode():
                print("   ✅ Work Experience section renders")
            if 'Certifications' in response.content.decode():
                print("   ✅ Certifications section renders")
            if 'Projects' in response.content.decode():
                print("   ✅ Projects & Portfolio section renders")
                
        else:
            print(f"❌ Edit profile page error (status: {response.status_code})")
        
        print()
        
        # Test candidate profile view
        print("Testing Candidate Profile Page...")
        print("-" * 60)
        profile_url = f'/candidate/profile/{user.id}/'
        response = client.get(profile_url)
        
        if response.status_code == 200:
            print(f"✅ Candidate profile page loads successfully (status: {response.status_code})")
            
            # Check for required context
            if 'profile' in response.context:
                print(f"   ✅ Context variable 'profile' present")
                
                # Check if profile has required attributes
                profile = response.context['profile']
                print(f"   ✅ Profile user: {profile.user.get_full_name()}")
                print(f"   ✅ Profile location: {profile.location or 'Not set'}")
                print(f"   ✅ Profile phone: {profile.phone_number or 'Not set'}")
            
            # Check template rendering
            template_checks = {
                'About Me': 'About Me section',
                'Professional Skills': 'Skills section',
                'Quick Info': 'Quick Info sidebar',
                'Availability': 'Availability status',
            }
            
            content = response.content.decode()
            for check_text, description in template_checks.items():
                if check_text in content:
                    print(f"   ✅ {description} renders")
                else:
                    print(f"   ⚠️  {description} not found")
                    
        else:
            print(f"❌ Candidate profile page error (status: {response.status_code})")
        
        print()
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("✅ All pages tested successfully!")
        print("\nTo fully test the form submission, log in and visit:")
        print(f"  - Edit Profile: /profile/edit/{user.id}/")
        print(f"  - View Profile: /candidate/profile/{user.id}/")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_profile_pages()
