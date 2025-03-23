from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
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
    coursethubmnail = models.FileField(upload_to='uploads/coursethumbnail/', null=True, blank=True) # must be image and not blank
    classnote = models.FileField(upload_to='uploads/classnote/', null=True, blank=True)
    coursecontent = models.FileField(upload_to='uploads/coursecontent/', null=True, blank=True)
    courseassessment = models.FileField(upload_to='upload/courseassessment/', null=True, blank=True)
    
# live class creaion
class ClassCreateform(models.Model):
    subjectName = models.CharField(max_length=50)
    duration = models.IntegerField()
    teacher =  models.ForeignKey(
        User,
        to_field='username',  # Use the username field as the foreign key
        on_delete=models.CASCADE,
        related_name="uploaded_class"
    )
    topic = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    for_class = models.CharField(max_length=10)
    joinLink = models.URLField(max_length=200)
    
    
# LWF Assessment Form    
class LWFAssessmentCreateform(models.Model):
    
    
    title = models.CharField(max_length=50)
    instruction = models.CharField(max_length=250)
    
    uploaded_by = models.ForeignKey(
        User,
        to_field='username',  # Use the username field as the foreign key
        on_delete=models.CASCADE,
        related_name="uploaded_assessment"
    )

    # Add current date field
    created_at = models.DateField( auto_now_add=True)

    # File uploaders for documents (e.g., Notes, thumbnails, video, ppt etc etc.)
    image = models.FileField(upload_to='uploads/LWFAssessment/', null=True, blank=True) # must be image and not blank
    
# LWF Deadline Management Assignment   
class DeadlineManagement(models.Model):
    
    
    topic = models.CharField(max_length=50)
    subject  = models.CharField(max_length=50)
    for_class = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    
    uploaded_by = models.ForeignKey(
        User,
        to_field='username',  # Use the username field as the foreign key
        on_delete=models.CASCADE,
        related_name="uploaded_assignment"
    )

    # Add current date field
    deadline = models.DateField()
    created_at = models.DateField( auto_now_add=True)
    # deadline
    

    # File uploaders for documents (e.g., Notes, thumbnails, video, ppt etc etc.)
    content = models.FileField(upload_to='uploads/LWFAssignment/') # must be image and not blank 
    def __str__(self):
        return f"Subject- {self.subject}, Topic- {self.topic}"  
    
# for student submission    
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        DeadlineManagement,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(
        User,  # Student who submitted the answer
        on_delete=models.CASCADE,
        related_name="submitted_assignments"
    )
    submitted_at = models.DateField(auto_now_add=True)
    answer_file = models.FileField(upload_to='uploads/LWFAssignment/Submissions/')

    def status(self):
        return "Submitted On Time" if self.submitted_at <= self.assignment.deadline else "Late Submission" 
    def __str__(self):
        return f"{self.topic} - {self.subject}"  
    
    
# Feedback form
class StudentReview(models.Model):
    student_name = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    review_message = models.TextField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    def __str__(self):
        return f"{self.student_name} - {self.rating} Stars"  
    
    
    
# Instructor Feedback form  
class InstructorFeedbackForm(models.Model):
    
    
    teacher_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    review_message = models.TextField(max_length=500)
    submitted_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    objects = models.Manager()

    
    def __str__(self):
        return f"{self.teacher_name} - {self.rating} Stars" 
          
          
          
