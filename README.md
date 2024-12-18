# LMS-Backend

AI BASED LEARNING MANAGEMENT SYSTEM FOR KIDS:: Backend Part

# This is Auth (Authorization) :: Login and Signup System for both the Students, Instructors and Admin

# Test Seperately as per Url Provided in the urls.py

# Use Postman Desktop for Testing all the REST APi

# Before that install and Configure the system properly

# Installation Guide::

1. Install Python 3.12.7 for Windows x64 link- https://www.python.org/downloads/
2. Create any Folder and inside that folder open VS code and clone this backend project.
   git clone https://github.com/CodeWithArghya/LMS-Backend.git
3. Install all dependencies like django, djangorest, djangojwt, djangomailer etc etc by running below command in terminal
   pip install -r requirements.txt

4. Download & Install, configure properly POstgreSQL RDBMS for Windows from this link- https://www.postgresql.org/download/windows/

5. After that run the following command in Project Base directory
   a) py manage.py makemigrations
   b) py manage.py migrate

6. To run the server ->> py manage.py runserver

7. Now check from 127.0.0.1/auth/XXXXXXXXXXX (as per url provided):: test accordingly as per the backend

# Any Problem/doubt ask me

# Do not modify/change anything in the source code

# After Testing API'S upload result in proper format, link will be provided later

# Testing will be done by Bapan withing 22/12/2024

# Rest APi Urls thats are required to check in POSTMAN Desktop(both input, output in json, auth validation: otp through email, error check)

# Details of APIS for auth of both student and instructors

1. http://127.0.0.1:8000/auth/student/register/ -> [POST method with JSON body- email, username, first_name, last_name, password, password2]
2. http://127.0.0.1:8000/auth/student/verify-otp/ -> [POST method with JSON body- email,otp] 6 digit otp will be sent in email inbox/spambox
   \*\* read the otp email & after verification see the verification email message also.
3. http://127.0.0.1:8000/auth/student/login/ -> [POST method with JSON body- username, password]
4. http://127.0.0.1:8000/auth/student/profile/ -> [GET method without any JSON body, but in header must provide access_token which you will get after login response as Bearer token....... and enable Authorization in header]

==== For Instructor 5. http://127.0.0.1:8000/auth/student/singnup/ -> [POST method with JSON body- email, username, first_name, last_name, password, password2] 6. http://127.0.0.1:8000/auth/student/otp-verify/ -> [POST method with JSON body- email,otp] 6 digit otp will be sent in email inbox/spambox
\*\* read the otp email & after verification see the verification email message also. 7. http://127.0.0.1:8000/auth/student/login/ -> [POST method with JSON body- username, password] 8. http://127.0.0.1:8000/auth/instructor/profile/ -> [GET method without any JSON body, but in header must provide access_token which you will get after login response as Bearer token....... and enable Authorization in header]

# Test all the APIS as per instructions above

# Test both the positive response and negtive response to check either all reponse and error messages are working properly or not

# save all the screenshots and share your test result in proper google form, link will be provied you here.

# Link of Google form to upload all result -
