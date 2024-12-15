from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
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
            from_email="codewitharghya0@gmail.com",
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

            # Validate OTP
            if temp_data.otp == int(otp):
                # Create the user
                user_data = temp_data.data
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=email,
                    password=user_data['password'],
                )
                user.save()

                
                
                subject = "Confirmation of Your Account in LMS"
                text_content = f"Welcome, {username} to LMS:: Digital Education to Your Child"
                html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
        <h2 style="text-align: center; color: #007bff;">Welcome to Digital LMS</h2>
        <p style="font-size: 16px; color: #555;">
            Congratulations! {username}, Your account has been successfully verified. You can now explore and enjoy our Digital LMS for free.
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
            from_email="codewitharghya0@gmail.com",
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
    
    

            
            
            
    