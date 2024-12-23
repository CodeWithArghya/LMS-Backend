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
urlpatterns = [
    
    path('auth/student/register/', views.UserSignup),
    path("auth/student/verify-otp/", views.VerifyOTP),
    path('auth/student/login/', views.UserLogin),
    path('auth/student/profile/',views.UserProfile),
    path('auth/instructor/signup/', views.InstructorSignup),
    path('auth/instructor/otp-verify/', views.OtpVerifyInstructor),
    path('auth/instructor/login/', views.InstructorLogin),
    path('auth/instructor/profile/', views.InstructorProfile),
    
]
