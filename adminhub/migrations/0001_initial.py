# Generated by Django 5.0.7 on 2024-09-22 04:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courseproficiencylevel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('deleted', models.BooleanField()),
                ('archived', models.BooleanField()),
            ],
            options={
                'db_table': 'courseproficiencylevel',
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('deleted', models.BooleanField()),
                ('archived', models.BooleanField()),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.BigIntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phoneno', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'instructors',
            },
        ),
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'invite_code',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('ic_number', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('student_remarks', models.TextField(blank=True, null=True)),
                ('guardian_salutation', models.CharField(max_length=10)),
                ('guardian_full_name', models.CharField(max_length=100)),
                ('guardian_relationship', models.CharField(max_length=50)),
                ('guardian_ic_number', models.CharField(max_length=20)),
                ('guardian_contact_number', models.CharField(max_length=20)),
                ('class_mode', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=100)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='receipts/')),
                ('agreements_check', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'adminhub_registration',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phoneno', models.CharField(blank=True, max_length=50, null=True)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('parentname', models.CharField(blank=True, max_length=200, null=True)),
                ('parentemail', models.CharField(blank=True, max_length=100, null=True)),
                ('parentphoneno', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('user_role', models.CharField(choices=[('administrator', 'Administrator'), ('instructor', 'Instructor'), ('student', 'Student')], default='student', max_length=13)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Coursewithproficiencylevel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('deleted', models.BooleanField()),
                ('archived', models.BooleanField()),
                ('courseid', models.ForeignKey(blank=True, db_column='courseid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.courses')),
                ('courseproficiencylevelid', models.ForeignKey(blank=True, db_column='courseproficiencylevelid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.courseproficiencylevel')),
            ],
            options={
                'db_table': 'coursewithproficiencylevel',
            },
        ),
        migrations.CreateModel(
            name='Coursewithproficiencylevellessons',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('deleted', models.BooleanField()),
                ('archived', models.BooleanField()),
                ('coursewithproficiencylevelid', models.ForeignKey(db_column='coursewithproficiencylevelid', on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.coursewithproficiencylevel')),
            ],
            options={
                'db_table': 'coursewithproficiencylevellessons',
            },
        ),
        migrations.CreateModel(
            name='Coursecontent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(blank=True, max_length=255, null=True)),
                ('filedata', models.BinaryField(blank=True, null=True)),
                ('minetype', models.CharField(blank=True, max_length=500, null=True)),
                ('fileextension', models.CharField(blank=True, max_length=10, null=True)),
                ('doctype', models.CharField(blank=True, max_length=100, null=True)),
                ('linkurl', models.TextField(blank=True, null=True)),
                ('coursewithproficiencylevellessonid', models.ForeignKey(blank=True, db_column='coursewithproficiencylevellessonid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.coursewithproficiencylevellessons')),
            ],
            options={
                'db_table': 'coursecontent',
            },
        ),
        migrations.CreateModel(
            name='Enrollments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('enrolmentdate', models.BigIntegerField(blank=True, null=True)),
                ('cancelled', models.BooleanField()),
                ('cancellationreason', models.CharField(blank=True, max_length=4000, null=True)),
                ('coursewithproficiencylevel', models.ForeignKey(blank=True, db_column='coursewithproficiencylevel', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.coursewithproficiencylevel')),
                ('studentid', models.ForeignKey(blank=True, db_column='studentid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.students')),
            ],
            options={
                'db_table': 'enrollments',
            },
        ),
        migrations.CreateModel(
            name='Enrolledcourselessons',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('coursewithproficiencylevellessonid', models.BigIntegerField(blank=True, null=True)),
                ('classdate', models.DateTimeField(blank=True, null=True)),
                ('classstarttime', models.DateTimeField(blank=True, null=True)),
                ('classendtime', models.DateTimeField(blank=True, null=True)),
                ('cancelled', models.BooleanField(blank=True, null=True)),
                ('enrollmentid', models.ForeignKey(blank=True, db_column='enrollmentid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.enrollments')),
                ('instructorid', models.ForeignKey(blank=True, db_column='instructorid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminhub.instructors')),
            ],
            options={
                'db_table': 'enrolledcourselessons',
            },
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('course_title', models.CharField(max_length=100)),
                ('class_mode', models.CharField(choices=[('online', 'Online'), ('physical', 'Physical'), ('hybrid', 'Hybrid')], max_length=20)),
                ('student_registration_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='adminhub.registration')),
            ],
            options={
                'db_table': 'student_course',
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminhub.users')),
            ],
            options={
                'db_table': 'password_reset_token',
            },
        ),
    ]
