#!/usr/bin/env python
"""
Test that employee dashboard does NOT show deleted jobs they applied to.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from jobapp.models import Job, Applicant

User = get_user_model()

def test_employee_dashboard_deleted_jobs():
    """Test that deleted jobs don't appear in employee dashboard."""
    client = Client()
    
    print("=" * 70)
    print("TESTING EMPLOYEE DASHBOARD - DELETED JOBS")
    print("=" * 70)
    print()
    
    # Get or create test employee
    employee = User.objects.filter(role='employee').first()
    if not employee:
        employee = User.objects.create_user(
            email='dash.emp@example.com',
            password='testpass123',
            first_name='Dashboard',
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
            email='dash-emp@example.com',
            password='testpass123',
            first_name='Dashboard',
            last_name='Employer',
            role='employer',
            gender='M'
        )
        print(f"✅ Created test employer: {employer.email} (ID: {employer.id})")
    else:
        print(f"✅ Found employer: {employer.email} (ID: {employer.id})")
    
    print()
    print("Test Setup: Creating jobs and applications...")
    print("-" * 70)
    
    # Create multiple jobs
    job1 = Job.objects.create(
        user=employer,
        title='Active Job',
        location='Remote',
        job_type='1',
        company_name='Test Corp',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False
    )
    print(f"✅ Created active job: {job1.title} (ID: {job1.id})")
    
    job2 = Job.objects.create(
        user=employer,
        title='To Be Deleted Job',
        location='Remote',
        job_type='1',
        company_name='Test Corp',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False
    )
    print(f"✅ Created job to be deleted: {job2.title} (ID: {job2.id})")
    
    print()
    print("Test 1: Employee applies to both jobs")
    print("-" * 70)
    
    # Employee applies to both jobs
    app1 = Applicant.objects.create(user=employee, job=job1)
    app2 = Applicant.objects.create(user=employee, job=job2)
    print(f"✅ Employee applied to job1 (Applicant ID: {app1.id})")
    print(f"✅ Employee applied to job2 (Applicant ID: {app2.id})")
    
    print()
    print("Test 2: Check employee dashboard (before deletion)")
    print("-" * 70)
    
    client.force_login(employee)
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        # Check applied jobs in dashboard
        applied_jobs = response.context.get('appliedjobs', [])
        print(f"✅ Dashboard loaded (status: {response.status_code})")
        print(f"   Applied jobs count: {len(applied_jobs)}")
        for app in applied_jobs:
            print(f"   - {app.job.title} (ID: {app.job.id}, is_deleted: {app.job.is_deleted})")
    else:
        print(f"❌ Dashboard failed to load (status: {response.status_code})")
        return
    
    print()
    print("Test 3: Employer deletes job2 (soft delete)")
    print("-" * 70)
    
    # Employer deletes job2 (soft delete)
    job2.is_deleted = True
    job2.deleted_at = timezone.now()
    job2.save()
    print(f"✅ Job2 soft-deleted: {job2.title}")
    print(f"   is_deleted: {job2.is_deleted}")
    print(f"   deleted_at: {job2.deleted_at}")
    
    # Verify job2 is marked as deleted
    job2_check = Job.all_objects.get(id=job2.id)
    print(f"   Verified in DB: is_deleted={job2_check.is_deleted}")
    
    print()
    print("Test 4: Check employee dashboard (after deletion)")
    print("-" * 70)
    
    # Refresh client and check dashboard again
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        applied_jobs = response.context.get('appliedjobs', [])
        print(f"✅ Dashboard loaded (status: {response.status_code})")
        print(f"   Applied jobs count: {len(applied_jobs)}")
        
        deleted_job_visible = False
        for app in applied_jobs:
            print(f"   - {app.job.title} (ID: {app.job.id}, is_deleted: {app.job.is_deleted})")
            if app.job.id == job2.id:
                deleted_job_visible = True
        
        print()
        if deleted_job_visible:
            print("❌ FAIL: Deleted job is STILL visible in employee dashboard!")
        else:
            print("✅ PASS: Deleted job is NOT visible in employee dashboard!")
    else:
        print(f"❌ Dashboard failed to load (status: {response.status_code})")
        return
    
    print()
    print("Test 5: Verify Applicant record still exists")
    print("-" * 70)
    
    applicants = Applicant.objects.filter(user=employee)
    print(f"✅ Employee applicant records: {applicants.count()}")
    for app in applicants:
        print(f"   - Applied to job: {app.job.title} (ID: {app.job.id}, is_deleted: {app.job.is_deleted})")
    
    print()
    print("=" * 70)
    print("✅ TEST COMPLETED!")
    print("=" * 70)

if __name__ == '__main__':
    test_employee_dashboard_deleted_jobs()
