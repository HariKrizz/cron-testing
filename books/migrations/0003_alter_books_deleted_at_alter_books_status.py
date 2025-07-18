# Generated by Django 5.2.1 on 2025-06-01 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_books_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='status',
            field=models.IntegerField(choices=[(1, 'Available'), (2, 'Returned'), (3, 'Reserved'), (4, 'Assigned'), (5, 'Deleted')], default=1, max_length=20),
        ),
    ]
