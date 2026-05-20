#!/usr/bin/env python
"""
Test employee viewing job detail page (the scenario that was failing).
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from jobapp.models import Job, Applicant

User = get_user_model()

def test_employee_view_applied_job():
    """Test employee viewing job detail page for a job they applied to."""
    client = Client()
    
    print("=" * 70)
    print("TESTING EMPLOYEE VIEWING JOB DETAIL PAGE")
    print("=" * 70)
    print()
    
    # Get or create test employee
    employee = User.objects.filter(role='employee').first()
    if not employee:
        employee = User.objects.create_user(
            email='emp.test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Employee',
            role='employee',
            gender='M'
        )
        print(f"✅ Created test employee: {employee.email} (ID: {employee.id})")
    else:
        print(f"✅ Found employee: {employee.email} (ID: {employee.id})")
    
    # Get or create test employer
    employer = User.objects.filter(role='employer').first()
    if not employer:
        employer = User.objects.create_user(
            email='emp-test@example.com',
            password='testpass123',
            first_name='Employer',
            last_name='Test',
            role='employer',
            gender='M'
        )
        print(f"✅ Created test employer: {employer.email} (ID: {employer.id})")
    else:
        print(f"✅ Found employer: {employer.email} (ID: {employer.id})")
    
    print()
    print("Creating test job...")
    print("-" * 70)
    
    # Create a published job from the employer
    job = Job.objects.create(
        user=employer,
        title='Test Job for Employee View',
        location='Remote',
        job_type='1',
        company_name='Test Corp',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False,
        description='Test job description'
    )
    print(f"✅ Created published job: {job.title} (ID: {job.id})")
    
    print()
    print("Test 1: Employee applies for job")
    print("-" * 70)
    
    # Employee applies for the job
    client.force_login(employee)
    application = Applicant.objects.create(
        user=employee,
        job=job
    )
    print(f"✅ Employee applied for job (Applicant ID: {application.id})")
    
    print()
    print("Test 2: Employee views job detail page")
    print("-" * 70)
    
    # Employee views the job detail page
    try:
        response = client.get(f'/job/{job.id}/')
        if response.status_code == 200:
            print(f"✅ Employee successfully viewed job detail page (status: {response.status_code})")
            print(f"   - Page title: {response.context.get('object').title if response.context else 'N/A'}")
            print(f"   - Related jobs count: {response.context.get('total', 'N/A') if response.context else 'N/A'}")
        else:
            print(f"❌ Failed to view job detail page (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Exception occurred: {type(e).__name__}: {str(e)}")
    
    print()
    print("=" * 70)
    print("✅ TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Job ID: {job.id}")
    print(f"  - Job Title: {job.title}")
    print(f"  - Is Published: {job.is_published}")
    print(f"  - Is Deleted: {job.is_deleted}")

if __name__ == '__main__':
    test_employee_view_applied_job()
