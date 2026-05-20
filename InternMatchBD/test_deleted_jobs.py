#!/usr/bin/env python
"""
Test script to verify deleted jobs no longer appear in dashboard after logout/login.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from jobapp.models import Job

User = get_user_model()

def test_deleted_job_removal():
    """Test that deleted jobs don't appear in employer dashboard."""
    client = Client()
    
    print("=" * 70)
    print("TESTING DELETED JOB REMOVAL FROM DASHBOARD")
    print("=" * 70)
    print()
    
    # Get or create test employer
    employer = User.objects.filter(role='employer').first()
    if not employer:
        employer = User.objects.create_user(
            email='test.employer@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Employer',
            role='employer',
            gender='M'
        )
        print(f"✅ Created test employer: {employer.email}")
    else:
        print(f"✅ Found existing employer: {employer.email} (ID: {employer.id})")
    
    print()
    
    # Create test jobs
    print("Creating test jobs...")
    job1 = Job.objects.create(
        user=employer,
        title='Test Job 1',
        location='New York',
        job_type='1',
        company_name='Test Company',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False
    )
    print(f"✅ Created job 1: {job1.title} (ID: {job1.id})")
    
    job2 = Job.objects.create(
        user=employer,
        title='Test Job 2 (To Delete)',
        location='New York',
        job_type='1',
        company_name='Test Company',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False
    )
    print(f"✅ Created job 2: {job2.title} (ID: {job2.id})")
    print()
    
    # Login and view dashboard
    print("Step 1: Login and view dashboard BEFORE deletion")
    print("-" * 70)
    client.force_login(employer)
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        jobs_before = response.context['jobs']
        print(f"✅ Dashboard loads (status: {response.status_code})")
        print(f"   Jobs visible before deletion: {len(jobs_before)}")
        for job in jobs_before:
            print(f"   - {job.title}")
    else:
        print(f"❌ Dashboard error (status: {response.status_code})")
    
    print()
    
    # Delete job2
    print("Step 2: Delete Job 2")
    print("-" * 70)
    job2.delete()  # This triggers soft delete
    job2.refresh_from_db()
    print(f"✅ Job 2 deleted (is_deleted={job2.is_deleted})")
    print()
    
    # Check database state
    print("Step 3: Check database (all objects including deleted)")
    print("-" * 70)
    all_jobs = Job.all_objects.filter(user=employer)
    print(f"Total jobs in DB (including deleted): {all_jobs.count()}")
    for job in all_jobs:
        status = "DELETED" if job.is_deleted else "ACTIVE"
        print(f"   - {job.title} [{status}]")
    print()
    
    # View dashboard while still logged in
    print("Step 4: View dashboard while logged in (should NOT show deleted)")
    print("-" * 70)
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        jobs_after = response.context['jobs']
        print(f"✅ Dashboard loads (status: {response.status_code})")
        print(f"   Jobs visible after deletion: {len(jobs_after)}")
        for job in jobs_after:
            print(f"   - {job.title}")
        
        # Check if deleted job appears
        deleted_job_visible = any(job.id == job2.id for job in jobs_after)
        if deleted_job_visible:
            print(f"\n❌ ERROR: Deleted job still visible in dashboard!")
        else:
            print(f"\n✅ CORRECT: Deleted job NOT visible in dashboard")
    else:
        print(f"❌ Dashboard error (status: {response.status_code})")
    
    print()
    
    # Logout and login again
    print("Step 5: Logout and login again")
    print("-" * 70)
    client.logout()
    print("✅ Logged out")
    
    client.force_login(employer)
    print("✅ Logged back in")
    print()
    
    # View dashboard after logout/login
    print("Step 6: View dashboard AFTER logout/login")
    print("-" * 70)
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        jobs_after_relogin = response.context['jobs']
        print(f"✅ Dashboard loads (status: {response.status_code})")
        print(f"   Jobs visible: {len(jobs_after_relogin)}")
        for job in jobs_after_relogin:
            print(f"   - {job.title}")
        
        # Final check
        deleted_job_visible = any(job.id == job2.id for job in jobs_after_relogin)
        if deleted_job_visible:
            print(f"\n❌ FAILED: Deleted job still visible after logout/login!")
        else:
            print(f"\n✅ SUCCESS: Deleted job NOT visible after logout/login!")
    else:
        print(f"❌ Dashboard error (status: {response.status_code})")
    
    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    test_deleted_job_removal()
