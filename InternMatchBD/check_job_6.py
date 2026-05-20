#!/usr/bin/env python
"""
Check if job 6 exists and what state it's in.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from jobapp.models import Job

print("=" * 70)
print("CHECKING JOB ID 6")
print("=" * 70)
print()

# Check in all objects (including deleted)
try:
    job_all = Job.all_objects.get(id=6)
    print(f"✅ Job found in database (all_objects):")
    print(f"   Title: {job_all.title}")
    print(f"   Is Deleted: {job_all.is_deleted}")
    print(f"   Deleted At: {job_all.deleted_at}")
    print(f"   Is Published: {job_all.is_published}")
    print(f"   Is Closed: {job_all.is_closed}")
    print()
    
    if job_all.is_deleted:
        print("❌ ERROR: Job 6 is SOFT-DELETED")
        print("   This job will return 404 with the new custom manager")
        print()
        print("SOLUTION:")
        print("   Option 1: Restore the job using hard_delete() or by setting is_deleted=False")
        print("   Option 2: Check if the job was intentionally deleted")
    
except Job.DoesNotExist:
    print("❌ Job 6 does not exist in database")
    print()
    print("Available jobs:")
    all_jobs = Job.all_objects.all()
    if all_jobs:
        for job in all_jobs[:10]:
            status = "DELETED" if job.is_deleted else "ACTIVE"
            print(f"   - Job {job.id}: {job.title} [{status}]")
    else:
        print("   No jobs in database")

print()

# Check if it's accessible via the active manager
print("Checking with active manager (Job.objects):")
try:
    job = Job.objects.get(id=6)
    print(f"✅ Job 6 is accessible via active manager")
except Job.DoesNotExist:
    print(f"❌ Job 6 is NOT accessible via active manager (it's deleted)")

