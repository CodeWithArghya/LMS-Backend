from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CourseCreateform(models.Model):
    class_choices = [
        ('preprimary', 'PrePrimary'),
        ('primary', 'Primary'),
        ('highschool', 'High School'),
        
    ]
    
    course_title = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    for_class = models.CharField(max_length=20, choices=class_choices)
    duration = models.CharField(max_length=15)  
    teacher_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    prerequites = models.CharField(max_length=100)
    course_outcomes = models.CharField(max_length=100)
    current_status = models.CharField(max_length=20, default='Pending')
    uploaded_by = models.ForeignKey(
        User,
        to_field='username',  # Use the username field as the foreign key
        on_delete=models.CASCADE,
        related_name="uploaded_courses"
    )


    # File uploaders for documents (e.g., Notes, thumbnails, video, ppt etc etc.)
    coursethubmnail = models.ImageField(upload_to='uploads/coursethumbnail/', null=True, blank=True) # must be image and not blank
    classnote = models.FileField(upload_to='uploads/classnote/', null=True, blank=True)
    coursecontent = models.FileField(upload_to='uploads/coursecontent/', null=True, blank=True)
    

