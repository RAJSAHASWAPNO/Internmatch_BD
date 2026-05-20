#!/usr/bin/env python
"""
Check if formsets are in template context.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def check_context():
    client = Client()
    
    user = User.objects.filter(role='employee').first()
    if not user:
        print("No test user found")
        return
    
    client.force_login(user)
    edit_url = f'/profile/edit/{user.id}/'
    response = client.get(edit_url)
    
    print("=" * 70)
    print("TEMPLATE CONTEXT")
    print("=" * 70)
    print()
    
    if hasattr(response, 'context') and response.context:
        print(f"Status Code: {response.status_code}")
        print(f"Total context keys: {len(response.context)}")
        print()
        
        print("Context variables:")
        for key in sorted(response.context.keys()):
            value = response.context[key]
            print(f"  - {key}: {type(value).__name__}")
            if key.endswith('_formset'):
                print(f"    Forms in formset: {len(value.forms)}")
                if value.forms:
                    print(f"    First form fields: {list(value.forms[0].fields.keys())}")
        
        # Check specific formsets
        print()
        print("Checking formsets...")
        for fs_name in ['education_formset', 'experience_formset', 'certification_formset', 'project_formset']:
            if fs_name in response.context:
                fs = response.context[fs_name]
                print(f"✅ {fs_name} found in context")
                print(f"   - Forms: {len(fs.forms)}")
                if hasattr(fs, 'management_form'):
                    print(f"   - Management form: {fs.management_form}")
                    print(f"   - Management form fields: {list(fs.management_form.fields.keys())}")
            else:
                print(f"❌ {fs_name} NOT in context")
    else:
        print("No context found!")

if __name__ == '__main__':
    check_context()
