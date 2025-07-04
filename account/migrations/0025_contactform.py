# Generated by Django 5.1.4 on 2025-03-27 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_rename_instructorfeedback_instructorfeedbackform'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('query_type', models.CharField(choices=[('generalquery', 'General Query'), ('report', 'Report'), ('help', 'Help/Support')], max_length=20)),
                ('contact', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='uploads/contact/')),
                ('submitted_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
