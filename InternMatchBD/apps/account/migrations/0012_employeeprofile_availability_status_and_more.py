

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_migrate_skills_to_skill_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='availability_status',
            field=models.CharField(choices=[('available', 'Available'), ('not_available', 'Not Available'), ('open_to_offers', 'Open to Offers')], default='available', max_length=20),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='languages',
            field=models.TextField(blank=True, help_text='Enter languages separated by commas or newlines'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='social_github',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='social_linkedin',
            field=models.URLField(blank=True),
        ),
        migrations.CreateModel(
            name='EmployeeCertification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('issuer', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('credential_url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='account.employeeprofile')),
            ],
            options={
                'ordering': ['-issue_date'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(help_text="e.g., Bachelor's, Master's, PhD", max_length=255)),
                ('field_of_study', models.CharField(max_length=255)),
                ('institution', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='account.employeeprofile')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='account.employeeprofile')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True)),
                ('technologies', models.CharField(blank=True, help_text='Enter technologies separated by commas', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='account.employeeprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
