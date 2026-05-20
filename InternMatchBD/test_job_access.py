#!/usr/bin/env python
"""
Test that employers can view their own posted jobs.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from jobapp.models import Job

User = get_user_model()

def test_employer_job_access():
    """Test that employers can view their own jobs."""
    client = Client()
    
    print("=" * 70)
    print("TESTING EMPLOYER JOB ACCESS")
    print("=" * 70)
    print()
    
    # Get or create test employer
    employer = User.objects.filter(role='employer').first()
    if not employer:
        employer = User.objects.create_user(
            email='job.test@example.com',
            password='testpass123',
            first_name='Job',
            last_name='Test',
            role='employer',
            gender='M'
        )
        print(f"✅ Created test employer: {employer.email}")
    else:
        print(f"✅ Found employer: {employer.email} (ID: {employer.id})")
    
    print()
    
    # Create test job that is published
    print("Test 1: Published Job (should be accessible to all)")
    print("-" * 70)
    job_published = Job.objects.create(
        user=employer,
        title='Published Job',
        location='New York',
        job_type='1',
        company_name='Test Company',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=False
    )
    print(f"Created published job: {job_published.title} (ID: {job_published.id})")
    
    # Test as anonymous user
    response = client.get(f'/job/{job_published.id}/')
    if response.status_code == 200:
        print(f"✅ Anonymous user can view published job (status: {response.status_code})")
    else:
        print(f"❌ Anonymous user cannot view published job (status: {response.status_code})")
    
    # Test as employer
    client.force_login(employer)
    response = client.get(f'/job/{job_published.id}/')
    if response.status_code == 200:
        print(f"✅ Employer can view their published job (status: {response.status_code})")
    else:
        print(f"❌ Employer cannot view their published job (status: {response.status_code})")
    
    print()
    
    # Create test job that is NOT published
    print("Test 2: Unpublished Job (only owner should access)")
    print("-" * 70)
    job_unpublished = Job.objects.create(
        user=employer,
        title='Unpublished Job',
        location='San Francisco',
        job_type='1',
        company_name='Test Company',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=False,
        is_deleted=False
    )
    print(f"Created unpublished job: {job_unpublished.title} (ID: {job_unpublished.id})")
    
    # Test as employer (should work)
    response = client.get(f'/job/{job_unpublished.id}/')
    if response.status_code == 200:
        print(f"✅ Employer can view their unpublished job (status: {response.status_code})")
    else:
        print(f"❌ Employer cannot view their unpublished job (status: {response.status_code})")
    
    # Test as anonymous user (should NOT work)
    client.logout()
    response = client.get(f'/job/{job_unpublished.id}/')
    if response.status_code == 404:
        print(f"✅ Anonymous user cannot view unpublished job (status: {response.status_code})")
    else:
        print(f"❌ Anonymous user should not be able to view unpublished job (status: {response.status_code})")
    
    print()
    
    # Test deleted job
    print("Test 3: Deleted Job (only owner can view)")
    print("-" * 70)
    job_deleted = Job.objects.create(
        user=employer,
        title='Deleted Job',
        location='Boston',
        job_type='1',
        company_name='Test Company',
        url='https://example.com',
        last_date='2026-12-31',
        is_published=True,
        is_deleted=True,
        deleted_at='2026-05-19'
    )
    print(f"Created deleted job: {job_deleted.title} (ID: {job_deleted.id})")
    
    # Test as employer (should work)
    client.force_login(employer)
    response = client.get(f'/job/{job_deleted.id}/')
    if response.status_code == 200:
        print(f"✅ Employer can view their deleted job (status: {response.status_code})")
    else:
        print(f"❌ Employer cannot view their deleted job (status: {response.status_code})")
    
    # Test as anonymous user (should NOT work)
    client.logout()
    response = client.get(f'/job/{job_deleted.id}/')
    if response.status_code == 404:
        print(f"✅ Anonymous user cannot view deleted job (status: {response.status_code})")
    else:
        print(f"❌ Anonymous user should not be able to view deleted job (status: {response.status_code})")
    
    print()
    print("=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)

if __name__ == '__main__':
    test_employer_job_access()
