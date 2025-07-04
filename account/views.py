from rest_framework import status
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions
from .serializers import RegisterSerializer, CourseSerial, ContactSerial, StudentReviewSerial, ClassSerial, LWFAssessmentSerial, DeadlineSerial, AssignmentSubmissionSerializer, InstructorReviewSerial
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
from account.models import CourseCreateform, ContactForm, ClassCreateform, LWFAssessmentCreateform, DeadlineManagement, AssignmentSubmission, StudentReview, InstructorFeedbackForm
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

        <p style="font-size: 16px; color: #D90000;">
            Click the button below to log in to your account & Its recommended to change your current password from your dashboard
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
    
@api_view(['POST'])
def InstructorLogin(request):
    try:
        data = request.data
        username = data.get("username")
        password = data.get("password")

        # Check if username or password is missing
        if not username or not password:
            return Response({"message": "Username and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Make sure username is a string and strip spaces
        username = str(username).strip()

        # Validate that username starts with 'INS'
        if not username.startswith("INS"):
            return Response({"message": "Only instructors can login. Invalid username format."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            # Generate token
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })

        return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": "Something went wrong", "error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# login for admin
# login & token
@api_view(['POST'])
def AdminLogin(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        password = data.get("password")
        if username == "principal":
            user = User.objects.filter(username = username).first()
            if user and user.check_password(password):
            #generate token
                refresh = RefreshToken.for_user(user)
                return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                
                
                })
        return Response({"message":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
 
import random
import string
    
# user forget password
# Function to generate a random password
def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@api_view(['POST'])
def UserForgetPassword(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        email = data.get("email")

        user = User.objects.filter(username=username, email=email).first()

        if not user:
            return Response({"message": "User does not exist or Email ID does ot match with our DB records. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new random password
        new_password = generate_random_password()

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Send email with the new password
        subject = "Password Reset Request"
        message = f"""
        Hello {user.username},

        Your new password is: {new_password} against User ID: {user.username}

        Please log in and change your password from dashboard immediately for security reasons.

        Regards,
        Learn With Fun Support Team
        """
        send_mail(subject, message, "eduhublmsofficials@gmail.com", [user.email])

        return Response({"message": "A new password has been sent to your email successfully."}, status=status.HTTP_200_OK)


# for changing password : for both student and instructor
@api_view(['POST'])
def UserChangePassword(request, username):
    data = request.data
    old_password = data.get("password")
    new_password = data.get("npass")
    confirm_password = data.get("cpass")

    # Check if user exists
    user = User.objects.filter(username=username).first()

    if not user:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Validate old password
    if not user.check_password(old_password):
        return Response({"message": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate new password match
    if new_password != confirm_password:
        return Response({"message": "New Password and Confirm Password must match."}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Your password has been changed successfully."}, status=status.HTTP_200_OK)

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


# feth all registered Student list to admin dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ViewStudentList(request):
    
    students = User.objects.filter(username__startswith="STD")
    serializer = RegisterSerializer(students, many=True)
    return Response({'registeredstudents':serializer.data}, status=status.HTTP_200_OK) 


# for delete student by admin
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def StudentDeleteByAdmin(request, id):
    # Fetch course uploaded by the specific instructor
    student = User.objects.filter(id=id,username__startswith="STD").first()

    if not student:
        return Response({'msg': 'No Student Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = RegisterSerializer(student)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        student.delete()  # Proper deletion
        return Response({'msg': 'Student Deleted Successfully'}, status=status.HTTP_200_OK)
    
# for delete instructor by admin
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def TeacherDeleteByAdmin(request, id):
    # Fetch course uploaded by the specific instructor
    student = User.objects.filter(id=id,username__startswith="INS").first()

    if not student:
        return Response({'msg': 'No Instructor Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = RegisterSerializer(student)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        student.delete()  # Proper deletion
        return Response({'msg': 'Instructor Deleted Successfully'}, status=status.HTTP_200_OK)    
# for delete query by admin
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def QueryDeleteByAdmin(request, id):
    # Fetch query
    query = ContactForm.objects.filter(id=id).first()

    if not query:
        return Response({'msg': 'No Query  Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = ContactSerial(query)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        query.delete()  # Proper deletion
        return Response({'msg': 'Query Deleted Successfully'}, status=status.HTTP_200_OK)  
# feth all registered Instructors list to admin dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ViewTeacherList(request):
    
    teachers = User.objects.filter(username__startswith="INS")
    serializer = RegisterSerializer(teachers, many=True)
    return Response({'registeredteachers':serializer.data}, status=status.HTTP_200_OK) 


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
    
# all pending course display to admin section only restricted to principal
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplayPendingCourses(request, username):

    if username != "principal":
        return Response({"msg": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
            
        courses = CourseCreateform.objects.filter(current_status="Pending")
        serial = CourseSerial(courses, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Course Found'}, status=status.HTTP_404_NOT_FOUND) 
    
# all approved course display to admin section only restricted to principal
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplayApprovedCourses(request, username):

    if username != "principal":
        return Response({"msg": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
            
        courses = CourseCreateform.objects.filter(current_status="Approved")
        serial = CourseSerial(courses, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Course Found'}, status=status.HTTP_404_NOT_FOUND) 
    
# all rejected course display to admin section only restricted to principal
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplayRejectedCourses(request, username):

    if username != "principal":
        return Response({"msg": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
            
        courses = CourseCreateform.objects.filter(current_status="Rejected")
        serial = CourseSerial(courses, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Course Found'}, status=status.HTTP_404_NOT_FOUND)  
    
# display total number of approved, pending and rejected courses to admin section only 
@api_view(['GET'])

def DisplayCourseCount(request):

   
    if request.method == "GET":
            
        approved_count = CourseCreateform.objects.filter(current_status="Approved").count()
        pending_count = CourseCreateform.objects.filter(current_status="Pending").count()
        rejected_count = CourseCreateform.objects.filter(current_status="Rejected").count() 
        
        return Response({
        "result": {
        "approved_count": approved_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count
    }
}, status=status.HTTP_200_OK)

    else:
        return Response({'msg':'Went Wrong'}, status=status.HTTP_404_NOT_FOUND)  
    
# display total number of registered Students and Instructors to Admin Panel
@api_view(['GET'])

def DisplayUserCount(request):

   
    if request.method == "GET":
            
        student = User.objects.filter(username__startswith="STD").count()
        instructors = User.objects.filter(username__startswith="INS").count()
        
         
        
        return Response({
        "result": {
        "student": student,
        "instructor": instructors,
        
    }
}, status=status.HTTP_200_OK)

    else:
        return Response({'msg':'Something Went Wrong'}, status=status.HTTP_404_NOT_FOUND)             

# admin approve course    
@api_view(['PATCH'])  # Using PATCH for partial updates
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ApproveCourse(request, username, id):
    
    if username != "principal":
        return Response({"msg": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
    try:
        # Fetch the course by ID
        course = CourseCreateform.objects.get(id=id)
        
        # Update the current_status field
        course.current_status = "Approved"
        course.save()

        return Response({"message": "Course approved successfully!"}, status=status.HTTP_200_OK)

    except CourseCreateform.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           

# admin approve course    
@api_view(['PATCH'])  # Using PATCH for partial updates
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def RejectCourse(request, username, id):
    
    if username != "principal":
        return Response({"msg": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
    try:
        # Fetch the course by ID
        course = CourseCreateform.objects.get(id=id)
        
        # Update the current_status field
        course.current_status = "Rejected"
        course.save()

        return Response({"message": "Course Rejected successfully!"}, status=status.HTTP_200_OK)

    except CourseCreateform.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
    
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
            external_api_url = "https://12y8sqod1g.execute-api.ap-south-1.amazonaws.com/default/classscheduled"

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

# display assessment uploaded by specific instructor
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DisplaySpecificAssessment(request, username):
    
    if request.method == "GET":
        assessment = DeadlineManagement.objects.filter(uploaded_by=username)
        serial = DeadlineSerial(assessment, many=True)
        return Response({'courses':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No Assessment Found'}, status=status.HTTP_404_NOT_FOUND) 
#specific assessments details
@api_view(['GET'])
def DisplayOneAssessments(request, id):
    try:
        assessments = DeadlineManagement.objects.get( id=id)
        serial = DeadlineSerial(assessments)  # No need for `many=True` as it's a single object
        return Response({'assessment': serial.data}, status=status.HTTP_200_OK)
    except DeadlineManagement.DoesNotExist:
        return Response({'msg': 'No Assessment Found'}, status=status.HTTP_404_NOT_FOUND)  
    
#assessments count
@api_view(['GET'])
def DisplayAssessmentsCount(request):
    try:
        assessments = DeadlineManagement.objects.count()
        
        return Response({'assessment': assessments}, status=status.HTTP_200_OK)
    except DeadlineManagement.DoesNotExist:
        return Response({
        "result": {
        "assessment":assessments,
        
    }
}, status=status.HTTP_404_NOT_FOUND)          
    
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
    return Response({'courses':serializer.data})

#sudent feedback submit (one email can be useed only once)
class StudentFeedback(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = StudentReviewSerial(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Review Submitted Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#contact submit to admin
class Contact(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data

        # Check if file exists in request.FILES
        files = request.FILES.get('attachments', None)

        # Merge files into data if exists
        if files:
            data['attachments'] = files

        serializer = ContactSerial(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Query Submitted Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
# number of queries    
@api_view(['GET'])

def DisplayQueryCount(request):
    
    if request.method == "GET":
        result = ContactForm.objects.count()
        
        return Response({'result':result}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Reviews Found'}, status=status.HTTP_404_NOT_FOUND)     
# displaying the student feedback to admin

@api_view(['GET'])

def DisplayStudentFeedback(request):
    
    if request.method == "GET":
        reviews = StudentReview.objects.all()
        serial = StudentReviewSerial(reviews, many=True)
        return Response({'studentreviews':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Reviews Found'}, status=status.HTTP_404_NOT_FOUND)  
    
# displaying the contact form to admin

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DisplayContactForm(request):
    
    if request.method == "GET":
        query = ContactForm.objects.all()
        serial = ContactSerial(query, many=True)
        return Response({'query':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Query Found'}, status=status.HTTP_404_NOT_FOUND)      
    
# instructor feedback    
class InstructorFeedback(APIView):
    
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data
        
        

        serializer = InstructorReviewSerial(data=data)  # Use the correct serializer
        if serializer.is_valid():
            serializer.save()  # Pass user object, not username
            
            
            return Response({'status': 'success', 'message': 'Feedback Submitted Successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
 # admin view of instructor feedback   
@api_view(['GET'])

def DisplayInstructorFeedback(request):
    
    if request.method == "GET":
        reviews = InstructorFeedbackForm.objects.all()
        serial = InstructorReviewSerial(reviews, many=True)
        return Response({'instructorreviews':serial.data}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':'No any Reviews Found'}, status=status.HTTP_404_NOT_FOUND)  
    


# ai based review analysis
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
import json
from .models import StudentReview  # make sure this import is correct

from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
import json
import re
from .models import StudentReview

@api_view(['GET'])
def analyze_review(request):
    # Get all review messages
    feedback_list = StudentReview.objects.values_list('review_message', flat=True)
    feedback_text = "\n".join(feedback_list)

    # Gemini API config
    api_key = "AIzaSyD9geiD-UIbtjlYr5RFPY6ZaDrktPlw648"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # Prompt
    prompt = (
    "You are an intelligent feedback analysis bot.\n\n"
    "Given multiple user reviews about a product, website, or service, your job is to:\n"
    "1. Generate a summary in under 100 words that reflects the overall sentiment and opinions.\n"
    "2. Classify each review as either 'positive' or 'negative'.\n\n"
    "Input is in the following JSON format:\n"
    "{reviews: ['Wonderful Product', 'I don't like it', 'Just Love this, awesome Product']}\n\n"
    "Output the result in JSON format:\n"
    "{summary: 'summary here', keywords: ['positive', 'negative', 'positive']}\n\n"
    f"Input: {feedback_text}"
)


    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            data = response.json()

            # Safely extract the text
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            if not text:
                return JsonResponse({"error": "No content returned by Gemini API"}, status=500)

            # Extract JSON from markdown-wrapped content
            json_match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
            if json_match:
                text = json_match.group(1).strip()

            try:
                parsed_response = json.loads(text)
                keywords = parsed_response.get("keywords", [])

                return JsonResponse({"keywords": keywords}, safe=False)

            except json.JSONDecodeError as e:
                return JsonResponse({
                    "error": f"Failed to parse JSON: {str(e)}",
                    "raw": text
                }, status=500)

        else:
            return JsonResponse(
                {"error": "Error from Gemini API", "details": response.text},
                status=response.status_code
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Network error", "details": str(e)}, status=500)

# fetch & display all user feedback in Admin Panel
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewfeedbackadmin(request):
    feedbacks = StudentReview.objects.all()
    serializer = StudentReviewSerial(feedbacks, many=True)
    return Response({'feedback':serializer.data}, status=status.HTTP_200_OK)  
 
# for delete feedback by admin
@api_view(['GET',  'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def FeedbackDeleteByAdmin(request, id):
    # Fetch query
    feedback = StudentReview.objects.filter(id=id).first()

    if not feedback:
        return Response({'msg': 'No feedback  Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serial = StudentReviewSerial(feedback)
        return Response(serial.data, status=status.HTTP_200_OK)

   

    elif request.method == "DELETE":
        feedback.delete()  # Proper deletion
        return Response({'msg': 'Feedback Deleted Successfully'}, status=status.HTTP_200_OK)
    
    
#assessments count
@api_view(['GET'])
def DisplayUserreviewCount(request):
    try:
        review = StudentReview.objects.count()
        
        
        return Response({'review': review}, status=status.HTTP_200_OK)
    except StudentReview.DoesNotExist:
        return Response({
        "result": {
        "review":review,
        
    }
}, status=status.HTTP_404_NOT_FOUND)  
        
        
        
# views.py
import pandas as pd


from .serializers import UserExcelRowSerializer

class UserExcelUploadAPIView(APIView):
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # read excel
            df = pd.read_excel(file_obj)

            required_columns = ['username','first_name', 'last_name', 'email', 'password', 'password2']
            if not all(col in df.columns for col in required_columns):
                return Response({"error": f"Excel must have columns: {', '.join(required_columns)}"}, status=400)

            created_users = []
            errors = []

            for index, row in df.iterrows():
                user_data = {
                      # Assuming 'id' is a unique identifier
                    'username': str(row['username']),
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': str(row['password']),
                    'password2': str(row['password2']),
                }

                serializer = UserExcelRowSerializer(data=user_data)
                if serializer.is_valid():
                    serializer.save()
                    created_users.append(user_data['username'])
                else:
                    errors.append({ 'row': index+2, 'errors': serializer.errors })

            return Response({
                'created_users': created_users,
                'errors': errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
