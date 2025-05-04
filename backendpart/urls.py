"""
URL configuration for backendpart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from rest_framework.routers import DefaultRouter
from account.views import CourseCreateAPIView,Contact, ClassCreateAPIView, LWFAssessmentCreateAPIView, DeadlineAssignment, StudentFeedback, InstructorFeedback



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/admin/login/', views.AdminLogin),
    path('auth/admin/profile/', views.InstructorProfile),
    path('api/admin/view-students/', views.ViewStudentList),
    path('api/admin/display-contact-query/', views.DisplayContactForm),
    path('api/admin/delete-student/<id>/', views.StudentDeleteByAdmin),
    path('api/admin/delete-instructor/<id>/', views.TeacherDeleteByAdmin),
    path('api/admin/delete-query/<id>/', views.QueryDeleteByAdmin),
    path('api/admin/view-instructors/', views.ViewTeacherList),
    path('auth/student/register/', views.UserSignup),
    path("auth/student/verify-otp/", views.VerifyOTP),
    path('auth/student/login/', views.UserLogin),
    path('auth/student/password-reset/', views.UserForgetPassword),
    path('auth/student/change-password/<username>/',views.UserChangePassword),
    path('auth/student/profile/',views.UserProfile),
    path('auth/instructor/signup/', views.InstructorSignup),
    path('auth/instructor/otp-verify/', views.OtpVerifyInstructor),
    path('auth/instructor/login/', views.InstructorLogin),
    path('auth/instructor/profile/', views.InstructorProfile),
    path('api/user-activity/', views.UserActivityAPIView),
    path('api/admin/approve-course/<username>/<id>/',views.ApproveCourse),
    path('api/admin/reject-course/<username>/<id>/',views.RejectCourse),
    path('api/allcourses/', views.DisplayCourses),
    path('api/coursedetails/<id>/', views.DisplayOneCourses),
    path('api/inscoursedetails/<id>/', views.INSDisplayOneCourses),
    path('api/assessmentdetails/<id>/', views.DisplayOneAssessments),
    path('api/coursemodify/<username>/<id>/', views.CourseEditByInstructor),
    path('api/instructor/assignment-modify/<username>/<id>/', views.AssignmentEditByInstructor),
    path('api/deletecourse/<username>/<id>/', views.CourseDeleteByInstructor),
    path('api/instructor/delete-assignment/<username>/<id>/', views.AssignmentDeleteByInstructor),
    path('api/specificcourses/<username>/', views.DisplaySpecificCourses),
    path('api/instructor/specificassessment/<username>/', views.DisplaySpecificAssessment),
    path('api/specificclasses/<username>/', views.DisplaySpecificClass),
    path('api/student/displayclasses/', views.DisplayClasses),
    path('api/user-activity/', views.UserActivityAPIView),
    path('api/displaystudentfeedback/', views.DisplayStudentFeedback),
    path('api/displayinstructorfeedback/', views.DisplayInstructorFeedback),
    path('api/object/', views.analyze_image),
    path('api/student/displaylwfassessment/', views.DisplayLWFAssessment),
    path('api/instructor/class-delete/<username>/<id>/', views.ClassDeleteByInstructor),
    path('api/instructor/create-course/', CourseCreateAPIView.as_view()),
    path('api/instructor/submit-feedback/', InstructorFeedback.as_view()),
    path('api/instructor/create-class/', ClassCreateAPIView.as_view()),
    path('api/student/feedback-submission/', StudentFeedback.as_view()),
    path('api/general/contactform-submission/', Contact.as_view()),
    path('api/student/display-assignments/', views.DisplayAssignment),
    path('api/instructor/create-lwf-assessment/', LWFAssessmentCreateAPIView.as_view()),
    path('api/instructor/create-assignment/', DeadlineAssignment.as_view()),
    path('api/home/dynamicdisplay/', views.DisplayTotalCourses),
    path('api/student/assignments/<int:id>/submit/', views.submit_assignment, name='submit-assignment'),
    path('api/instructor/view-submissions/', views.teacher_submissions, name='teacher-submissions'),
    path('api/admin/display-pending-courses/<username>/', views.DisplayPendingCourses),
    path('api/admin/display-approved-courses/<username>/', views.DisplayApprovedCourses),
    path('api/admin/display-rejected-courses/<username>/', views.DisplayRejectedCourses),
    path('api/aireview-analysis/', views.analyze_review), 
   
    
]
