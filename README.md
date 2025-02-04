# LMS-Backend

AI BASED LEARNING MANAGEMENT SYSTEM FOR KIDS:: Backend Part

# This is Course Create/Modify/Get test for API for Instructors & Students

# Test Seperately as per Url Provided in the urls.py

# Use Postman Desktop for Testing all the REST APi

# Before that install and Configure the system properly

# Installation Guide::

1. Use SQL file provided in Whatsapp Group & Import that SQL file in your local Postgresql DB.
2. Pull Updated Code from this repo.
3. Run > py manage.py makemigrations
4. Run > py manage.py migrate
5. To run the server ->> py manage.py runserver
6. Now check from 127.0.0.1/auth/XXXXXXXXXXX (as per url provided):: test accordingly as per the backend

# Any Problem/doubt ask me:: I am ready for assisting you

# Do not modify/change anything in the source code

# After Testing API'S upload result in proper format, link will be provided later

# Testing will be done by Bapan withing 22/12/2024

# Rest APi Urls thats are required to check in POSTMAN Desktop(both input, output in json, auth validation: otp through email, error check)

# Details of APIS for auth of both student and instructors

# Login first as a instructor / student
1. http://127.0.0.1:8000/api/allcourses/ -> [GET method without any JSON body, but in header must provide access_token which you will get after login response as Bearer token....... and enable Authorization in header]
2. http://127.0.0.1:8000/api/instructor/create-course/ -> [POST method with JSON body- course_title,subject_name,for_class (e.g- primary),duration,  teacher_name,description,prerequites,course_outcomes,current_status, uploaded_by,
    # File uploaders for documents (e.g., Notes, thumbnails, video, ppt etc etc.) *** Use Formdata in POstman
    coursethubmnail, classnote, coursecontent]

3. http://127.0.0.1:8000/api/coursemodify/<username>/<id>/ -> [PUT method with JSON body- same as create-course] # provide username and courseid (after login)
4.  http://127.0.0.1:8000/api/specificcourses/<username>/-> [GET method] # provide any specific username along with access_token in header after login

# Test all the APIS as per instructions above

# Test both the positive response and negtive response to check either all reponse and error messages are working properly or not

# save all the screenshots and share your test result in our official Whatsapp Group.

# Last date for Test Case Result Submission is ->> 06.02.2025
All The Best +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
