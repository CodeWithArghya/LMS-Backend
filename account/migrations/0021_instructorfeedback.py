# Generated by Django 5.1.4 on 2025-03-23 18:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_studentreview'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('review_message', models.TextField(max_length=500)),
                ('submitted_at', models.DateField(auto_now_add=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_feedback', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]
