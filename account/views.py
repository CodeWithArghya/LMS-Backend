from rest_framework import status
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions
from .serializers import RegisterSerializer, CourseSerial,ClassSerial, LWFAssessmentSerial, DeadlineSerial, AssignmentSubmissionSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
from account.models import CourseCreateform, ClassCreateform, LWFAssessmentCreateform, DeadlineManagement, AssignmentSubmission
from django.core.cache import cache 
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# Create your views here.

from django.db import models

class TemporaryUserData(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    data = models.JSONField()  # Store user details like username, password
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



@api_view(['POST'])
def UserSignup(request):
    if request.method == "POST":
        data = request.data
        serializer = RegisterSerializer(data=data)

        # Validate input data
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']
            password2 = data.get('password2')

            # Ensure passwords match
            if password != password2:
                return Response(
                    {"message": "Passwords do not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store data temporarily
            TemporaryUserData.objects.update_or_create(
                email=email,
                defaults={
                    "otp": otp,
                    "data": {
                        "username": username,
                        "password": password,
                        "first_name":first_name,
                        "last_name":last_name
                    },
                },
            )

            # Send OTP email
            subject = "Your OTP for Account Verification"
            text_content = f"Your OTP is: {otp}. Verify your account with this OTP to enjoy LMS."
            html_content = f"""
    <p>Your OTP is: <strong>{otp}</strong>.</p>
    <p>Verify your account with this OTP to enjoy LMS.</p>
    <a href="http://localhost:3000/" style="
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #fff;
        background-color: #007bff;
        border-radius: 5px;
        text-decoration: none;
        border: 1px solid #007bff;
        font-weight: bold;
    ">
        Click Here to Login Your Account
    </a>
"""
            email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text version (fallback)
            from_email="eduhublmsofficilas@gmail.com",
            to=[email],
            )

            # Attach the HTML version
            email_message.attach_alternative(html_content, "text/html")

# Send the email
            email_message.send(fail_silently=False)    

            return Response(
                {"message": "OTP sent to your email."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# verify OTP


@api_view(['POST'])
def VerifyOTP(request):
    if request.method == "POST":
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            # Fetch the temporary data
            temp_data = TemporaryUserData.objects.get(email=email)

            username = temp_data.data.get('username')
            password = temp_data.data.get('password')
            first_name = temp_data.data.get('first_name')
            last_name = temp_data.data.get('last_name')
            # Validate OTP
            if temp_data.otp == int(otp):
                # Create the user
                user_data = temp_data.data
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=email,
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                user.save()

                
                
                subject = "Confirmation of Your Account in LMS"
                text_content = f"Welcome, {first_name} {last_name} to LMS:: Digital Education to Your Child"
                html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
        <h2 style="text-align: center; color: #007bff;">Welcome to Digital LMS</h2>
        <p style="font-size: 16px; color: #555;">
            Congratulations! {first_name} {last_name}, Your account has been successfully verified. You can now explore and enjoy our Digital LMS for free.
        </p>
        
        <p style="
    font-size: 16px; 
    color: #FF0000; 
    background-color: #FFECEC; 
    padding: 10px; 
    border: 1px solid #FFCCCC; 
    border-radius: 5px; 
    font-weight: bold; 
    font-family: Arial, sans-serif;
    text-align: center;">
    Login in System with Username: <span style="color: #D90000;">{username}</span>, 
    Password: <span style="color: #D90000;">{password}</span>
</p>

        <p style="font-size: 16px; color: #555;">
            Click the button below to log in to your account and start your learning journey.
        </p>
        <a href="http://localhost:3000/" style="
            display: block;
            width: fit-content;
            margin: 20px auto;
            text-align: center;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
            border: 1px solid #007bff;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            Click Here to Login Your Account
        </a>
        <p style="font-size: 14px; text-align: center; color: #999;">
            If you didn't register for this service, please ignore this email or contact with us by reply in this mail.
        </p>
    </div>
"""

                email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text version (fallback)
            from_email="eduhublmsofficials@gmail.com",
            to=[email],
            )

            # Attach the HTML version
                email_message.attach_alternative(html_content, "text/html")

# Send the email
                email_message.send(fail_silently=False)
                # Clean up temporary data
                temp_data.delete()
                return Response(
                    {"message": "Account verified and created successfully!"},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"message": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except TemporaryUserData.DoesNotExist:
            return Response(
                {"message": "No OTP request found for this email."},
                status=status.HTTP_404_NOT_FOUND,
            )



# login & token
@api_view(['POST'])
def UserLogin(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = User.objects.filter(username = username).first()
        if user and user.check_password(password):
            #generate token
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                
                
            })
        return Response({"message":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)    
            
            
    
# profile access by token only
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data) 
 
    
# signup, login and profile for Instructor of LMS

#signup for Instructors
@api_view(['POST'])
def InstructorSignup(request):
    if request.method == "POST":
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        # validation of data
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']
            password2 = data.get('password2')
            
            #password validation
            if password != password2:
                return Response(
                    {'message':'Password is not matched with Confirm Password'}, status=status.HTTP_400_BAD_REQUEST)
            
            #otp
            otp = random.randint(100000, 999999)
            
            #store data temporary
            TemporaryUserData.objects.update_or_create(
                email=email,
                defaults={
                    "otp":otp,
                    "data":{
                        "username":username,
                        "first_name":first_name,
                        "last_name":last_name,
                        "password":password
                    }
                }
            )
            
             # Send OTP email
            subject = "Your OTP for Instructor Account Verification"
            text_content = f"Your OTP is: {otp}. Verify your account with this OTP to access LMS for uploading Contents."
            html_content = f"""
    <p>Your OTP is: <strong>{otp}</strong>.</p>
    <p>Verify your account with this OTP to access LMS for uploading Contents</p>
    <a href="http://localhost:3000/login" style="
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #fff;
        background-color: #007bff;
        border-radius: 5px;
        text-decoration: none;
        border: 1px solid #007bff;
        font-weight: bold;
    ">
        Click Here to Login Your Account
    </a>
"""
            email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text version (fallback)
            from_email="eduhublmsofficials@gmail.com",
            to=[email],
            )

            # Attach the HTML version
            email_message.attach_alternative(html_content, "text/html")

# Send the email
            email_message.send(fail_silently=False)    

            return Response(
                {"message": "OTP sent to your email. Check Inbox/Spambox"},
                status=status.HTTP_200_OK,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

#otp verify and account creation of instructors
@api_view(['POST'])
def OtpVerifyInstructor(request):
    if request.method == "POST":
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        # fetch the data from temp
        try:
            temp_data = TemporaryUserData.objects.get(email=email)
            username = temp_data.data.get('username')
            password = temp_data.data.get('password')
            first_name = temp_data.data.get('first_name')
            last_name =  temp_data.data.get('last_name')
            
            if temp_data.otp == int(otp):
                user_data = temp_data.data
                user = User.objects.create_user(
                    username= user_data['username'],
                    email=email,
                    password= user_data['password'],
                    first_name = user_data['first_name'],
                    last_name = user_data['last_name']
                    
                )
                user.save()
                subject = "Confirmation of Your Instructor Account in LMS"
                text_content = f"Welcome, {first_name} {last_name} to LMS:: Digital Education to Your Child"
                html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
        <h2 style="text-align: center; color: #007bff;">Welcome to Digital LMS</h2>
        <p style="font-size: 16px; color: #555;">
            Congratulations! {first_name} {last_name}, Your Instructor account has been successfully verified. You can now explore and enjoy our Digital LMS for free by uploading your contents for childs.
        </p>
        
        <p style="
    font-size: 16px; 
    color: #FF0000; 
    background-color: #FFECEC; 
    padding: 10px; 
    border: 1px solid #FFCCCC; 
    border-radius: 5px; 
    font-weight: bold; 
    font-family: Arial, sans-serif;
    text-align: center;">
    Login in System with Username: <span style="color: #D90000;">{username}</span>, 
    Password: <span style="color: #D90000;">{password}</span>
</p>

        <p style="font-size: 16px; color: #555;">
            Click the button below to log in to your account and start your teaching journey.
        </p>
        <a href="http://localhost:3000/login" style="
            display: block;
            width: fit-content;
            margin: 20px auto;
            text-align: center;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
            border: 1px solid #007bff;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            Click Here to Login Your Account
        </a>
        <p style="font-size: 14px; text-align: center; color: #999;">
            If you face any issue while login, please feel free to  contact with us by reply in this mail.
        </p>
    </div>
"""

                email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text version (fallback)
            from_email="eduhublmsofficials@gmail.com",
            to=[email],
            )

            # Attach the HTML version
                email_message.attach_alternative(html_content, "text/html")

# Send the email
                email_message.send(fail_silently=False)
                # Clean up temporary data
                temp_data.delete()
                return Response(
                    {"message": "Instructor Account verified and created successfully!"},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"message": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except TemporaryUserData.DoesNotExist:
            return Response(
                {"message": "No OTP request found for this email."},
                status=status.HTTP_404_NOT_FOUND,
            )
# login and token generation for the instructors

@api_view(['POST'])
def InstructorLogin(request):
    if request.method == "POST":
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }
            )
        return Response({'message':'Invalid Credentials, try Again'}, status=status.HTTP_400_BAD_REQUEST)    

# Instructor profile access by token only
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def InstructorProfile(request):
    
    user = request.user
    serializer = RegisterSerializer(user)
    return Response(serializer.data) 


# security features to track user activity
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UserActivityAPIView(request):
    user = request.user
    tab_switch_key = f"tab_switch_count_{user.id}"

    # Increment the tab switch count
    tab_switch_count = cache.get(tab_switch_key, 0) + 1
    cache.set(tab_switch_key, tab_switch_count, timeout=3600)  # Store for 1 hour

    # Prepare the default email data
    subject = 'Your Kids Browser Activity Detected'
    message = f"Your Child->> {user.username} has switched browser tabs or closed the browser."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    # Check if the tab switch count exceeds the danger threshold
    if tab_switch_count > 5:
        subject = 'Danger: Frequent Tab Switching Detected'
        message = (
            f"Your Child->> {user.username} has switched browser tabs {tab_switch_count} times. "
            "This could indicate a lack of focus.Please take care."
        )
    
    try:
        send_mail(subject, message, from_email, recipient_list)

        # If count exceeds threshold, reset it to avoid spamming
        if tab_switch_count > 5:
            cache.set(tab_switch_key, 0, timeout=3600)  # Reset the counter

        return Response({'status': 'success', 'message': 'Email notification sent.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 'error', 'message': 'Failed to send email notification.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
from rest_framework.parsers import MultiPartParser, FormParser  
class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['uploaded_by'] = request.user.username
        
        
        
        
        serializer = CourseSerial(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Course added, but email could not be sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# all courses dsiplay to athenticated users if the courses is approved by admin
@api_view(['GET'])

def DisplayCourses(request):
    
    if request.method == "GET":
        courses = CourseCreateform.objects.filter(current_status="Approved")
        serial = CourseSerial(courses, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Course Found'}, status=status.HTTP_404_NOT_FOUND)
    
#specific course details
@api_view(['GET'])
def DisplayOneCourses(request, id):
    try:
        course = CourseCreateform.objects.get(current_status="Approved", id=id)
        serial = CourseSerial(course)  # No need for `many=True` as it's a single object
        return Response({'course': serial.data}, status=status.HTTP_200_OK)
    except CourseCreateform.DoesNotExist:
        return Response({'msg': 'No Course Found'}, status=status.HTTP_404_NOT_FOUND)  
   
# for instructor
#specific course details
@api_view(['GET'])
def INSDisplayOneCourses(request, id):
    try:
        course = CourseCreateform.objects.get( id=id)
        serial = CourseSerial(course)  # No need for `many=True` as it's a single object
        return Response({'course': serial.data}, status=status.HTTP_200_OK)
    except CourseCreateform.DoesNotExist:
        return Response({'msg': 'No Course Found'}, status=status.HTTP_404_NOT_FOUND)      
# display courses uploaded by specific instructor
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplaySpecificCourses(request, username):
    
    if request.method == "GET":
        courses = CourseCreateform.objects.filter(uploaded_by=username)
        serial = CourseSerial(courses, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Course Found'}, status=status.HTTP_404_NOT_FOUND) 
    
@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def CourseEditByInstructor(request, username, id):
    # Fetch course uploaded by the specific instructor
    course = CourseCreateform.objects.filter(id=id, uploaded_by=username).first()

    if not course:
        return Response({'msg': 'No Course Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = CourseSerial(course)
        return Response({'course': serial.data}, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        
        data = request.data.copy()
        data['uploaded_by'] = request.user.username
        
        
        serial = CourseSerial(course, data=request.data, partial=True)  # Allows partial updates
        if serial.is_valid():
            serial.save()
            
            return Response({'msg': 'Course Updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)       
    
        
# for delete
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def CourseDeleteByInstructor(request, username, id):
    # Fetch course uploaded by the specific instructor
    course = CourseCreateform.objects.filter(id=id, uploaded_by=username).first()

    if not course:
        return Response({'msg': 'No Course Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = CourseSerial(course)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        course.delete()  # Proper deletion
        return Response({'msg': 'Course Deleted Successfully'}, status=status.HTTP_200_OK)
   
    
# class Scheudle
class ClassCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['teacher'] = request.user.username

        serializer = ClassSerial(data=data)
        if serializer.is_valid():
            serializer.save()

            # ✅ Send a POST request to the external API (no payload)
            external_api_url = "https://wcsp440x1d.execute-api.ap-south-1.amazonaws.com/default/ParentsMeet/demo"

            try:
                requests.post(external_api_url, timeout=20)  # ✅ No data sent, just a POST request
            except requests.exceptions.RequestException as e:
                return Response({
                    "status": "error",
                    "message": "Class scheduled, but external API request failed.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'status': 'success',
                'message': 'Live Class Scheduled Successfully.'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# display classes uploaded by specific instructor
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplaySpecificClass(request, username):
    
    if request.method == "GET":
        classes = ClassCreateform.objects.filter(teacher=username)
        serial = ClassSerial(classes, many=True)
        return Response({'classes':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Class is Scheduled Yet'}, status=status.HTTP_404_NOT_FOUND) 
                       
                       
# all sechulded class data for displaging in the student dashboard
@api_view(['GET'])

def DisplayClasses(request):
    
    if request.method == "GET":
        classes = ClassCreateform.objects.all()
        serial = ClassSerial(classes, many=True)
        return Response({'classes':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'Class not yet Scheduled'}, status=status.HTTP_404_NOT_FOUND)                       
    
      
# for delete a class
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ClassDeleteByInstructor(request, username, id):
    # Fetch course uploaded by the specific instructor
    classes = ClassCreateform.objects.filter(id=id, teacher=username).first()

    if not classes:
        return Response({'msg': 'No Class Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = ClassSerial(classes)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        classes.delete()  # Proper deletion
        return Response({'msg': 'Class Deleted Successfully'}, status=status.HTTP_200_OK)    
    
# counting total courses
@api_view(['GET'])

def DisplayTotalCourses(request):
    
    if request.method == "GET":
        total_courses = CourseCreateform.objects.count()
        total_students = User.objects.filter(username__startswith="STD").count()
        total_ins = User.objects.filter(username__startswith="INS").count()
        
        return Response(
            {
                'totalcourses': total_courses,
                'totalstudents': total_students,
                'totalins':total_ins
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response({'msg':'No course found'}, status=status.HTTP_404_NOT_FOUND)   


# LWF Assessment for the Instructor    
class LWFAssessmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        
        data['uploaded_by'] = request.user.username  # Ensure correct foreign key reference

        serializer = LWFAssessmentSerial(data=data)  # Use the correct serializer
        if serializer.is_valid():
            serializer.save()  # Pass user object, not username
            return Response({'status': 'success', 'message': 'Assessment added successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# displaying the assessment to the student section

@api_view(['GET'])

def DisplayLWFAssessment(request):
    
    if request.method == "GET":
        lwf = LWFAssessmentCreateform.objects.all()
        serial = LWFAssessmentSerial(lwf, many=True)
        return Response({'assessments':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Assessment Found'}, status=status.HTTP_404_NOT_FOUND)  
    
    
# image analysis & User Activity
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Enforces authentication
def UserActivityAPIView(request):
    user = request.user

    if not user.is_authenticated:
        return Response({'status': 'error', 'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    email = user.email

    subject = 'User Activity Detected'
    message = f"User {user.first_name} {user.last_name} has switched browser tabs or closed the browser during Assessment/Quize."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        return Response({'status': 'success', 'message': 'Email notification sent.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import json
import base64
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
def analyze_image(request):
    if 'image' not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)

    image_file = request.FILES['image']
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    api_key = "AIzaSyD9geiD-UIbtjlYr5RFPY6ZaDrktPlw648"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Identify the picture and generate 20 easy question answer about it for 5 years old kids in proper JSON format"},
                    {"inline_data": {"mime_type": "image/png", "data": base64_image}}
                ]
            }
        ]
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            data = response.json()

            # Extract the raw text content from the API response
            text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

           

            # Check if 'text' has the expected JSON string format
            if text.startswith("```json\n") and text.endswith("\n```"):
                text = text[len("```json\n"): -len("\n```")]

            

            # Now try to parse the cleaned-up text
            try:
                # Parse the JSON response from the text
                parsed_response = json.loads(text)

                # Extract the picture and qa fields
                picture = parsed_response.get("picture", "")
                qa = parsed_response.get("questions", [])

                # Format the response to match the desired structure
                formatted_response = {
                    "question": picture,
                    "ans": [{"question": qa_item.get("question"), "answer": qa_item.get("answer")} for qa_item in qa]
                }

                

                # Return the formatted response as JSON
                return JsonResponse(formatted_response, safe=False)

            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                return JsonResponse({"error": f"Failed to parse JSON: {str(e)}"}, status=500)

        else:
            return JsonResponse(
                {"error": "Error analyzing the image", "details": response.text},
                status=response.status_code
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Network error", "details": str(e)}, status=500)
    
    
    
# LWF Deadline Management for Instructor  
class DeadlineAssignment(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        
        data['uploaded_by'] = request.user.username  # Ensure correct foreign key reference

        serializer = DeadlineSerial(data=data)  # Use the correct serializer
        if serializer.is_valid():
            serializer.save()  # Pass user object, not username
            # ✅ Send a POST request to the external API (no payload)
            external_api_url = "https://wcsp440x1d.execute-api.ap-south-1.amazonaws.com/default/ParentsMeet/demo" # api have to change accordingly

            try:
                requests.post(external_api_url, timeout=20)  # ✅ No data sent, just a POST request
            except requests.exceptions.RequestException as e:
                return Response({
                    "status": "error",
                    "message": "Asssigment Send, but external API request failed.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'status': 'success', 'message': 'Assignment added successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
   
# modify assignment deadlines    
@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def AssignmentEditByInstructor(request, username, id):
    # Fetch assigmnet uploaded by the specific instructor
    assignment = DeadlineManagement.objects.filter(id=id, uploaded_by=username).first()

    if not assignment:
        return Response({'msg': 'No Assignment Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = DeadlineSerial(assignment)
        return Response({'assignment': serial.data}, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        
        data = request.data.copy()
        data['uploaded_by'] = request.user.username
        
        
        serial = DeadlineSerial(assignment, data=request.data, partial=True)  # Allows partial updates
        if serial.is_valid():
            serial.save()
            
            return Response({'msg': 'Assignment Updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)      
# displaying the assessment to the student section

@api_view(['GET'])

def DisplayAssignment(request):
    
    if request.method == "GET":
        assignment = DeadlineManagement.objects.all()
        serial = DeadlineSerial(assignment, many=True)
        return Response({'assessments':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Assignment Found'}, status=status.HTTP_404_NOT_FOUND)  
    
    
# for delete
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def AssignmentDeleteByInstructor(request, username, id):
    # Fetch course uploaded by the specific instructor
    assignment = DeadlineManagement.objects.filter(id=id, uploaded_by=username).first()

    if not assignment:
        return Response({'msg': 'No Assignment Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = DeadlineSerial(assignment)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        assignment.delete()  # Proper deletion
        return Response({'msg': 'Assignment Deleted Successfully'}, status=status.HTTP_200_OK)
       
#SUBMIT AN ASSIGNMENT (Only Students)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_assignment(request, id):
    assignment = get_object_or_404(DeadlineManagement, id=id)

    serializer = AssignmentSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        
        serializer.save(student=request.user, assignment=assignment)  # Assign student & assignment
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TEACHERS CAN VIEW SUBMISSIONS FOR THEIR ASSIGNMENTS ONLY
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def teacher_submissions(request):
    """Teachers can only see submissions for assignments they uploaded."""
    user = request.user
    if not user.uploaded_assignment.exists():
        return Response({"message": "You haven't uploaded any assignments yet."})

    submissions = AssignmentSubmission.objects.filter(assignment__uploaded_by=user)
    serializer = AssignmentSubmissionSerializer(submissions, many=True)
    return Response(serializer.data)