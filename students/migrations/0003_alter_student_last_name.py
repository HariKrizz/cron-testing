# Generated by Django 5.2.1 on 2025-06-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
