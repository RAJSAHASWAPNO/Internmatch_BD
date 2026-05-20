#!/usr/bin/env python
"""
Test to view actual HTML output of the form.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def view_form_html():
    client = Client()
    
    user = User.objects.filter(role='employee').first()
    if not user:
        return
    
    client.force_login(user)
    edit_url = f'/profile/edit/{user.id}/'
    response = client.get(edit_url)
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # Find and print management form
        import re
        
        print("=" * 70)
        print("MANAGEMENT FORM CONTENT")
        print("=" * 70)
        
        # Extract management form for each formset
        for formset_name in ['education', 'experience', 'certification', 'project']:
            print(f"\n{formset_name.upper()} FORMSET:")
            print("-" * 70)
            
            # Find management form
            pattern = f'name="{formset_name}-TOTAL_FORMS"'
            if pattern in content:
                # Get context around the pattern
                idx = content.find(pattern)
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                print(content[start:end])
                print("✅ Found TOTAL_FORMS field")
            else:
                print(f"❌ NOT FOUND: {pattern}")
            
            # Check for other management fields
            for field in ['INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS']:
                pattern = f'name="{formset_name}-{field}"'
                if pattern in content:
                    print(f"✅ Found {field}")
                else:
                    print(f"❌ Missing {field}")
        
        # Also print a sample of the form HTML to see the structure
        print("\n" + "=" * 70)
        print("FIRST 2000 CHARS OF FORM")
        print("=" * 70)
        
        form_start = content.find('<form')
        if form_start >= 0:
            form_end = form_start + 2000
            print(content[form_start:form_end])

if __name__ == '__main__':
    view_form_html()
