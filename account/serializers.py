from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import CourseCreateform, ClassCreateform, LWFAssessmentCreateform, DeadlineManagement, AssignmentSubmission


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    # Validate both password and first_name/last_name
    def validate(self, data):
        if isinstance(data.get('first_name'), list):
            data['first_name'] = data['first_name'][0]
        if isinstance(data.get('last_name'), list):
            data['last_name'] = data['last_name'][0]
    
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password and Confirm Password must be the same.")
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("First name and Last name must not be the same.")
        return data

    
    

    # Create user with hashed password
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not needed for user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user
    
#for create course
class CourseSerial(serializers.ModelSerializer):
    class Meta:
        model = CourseCreateform
        fields = '__all__'
    
    def validate(self, data):
        if data['course_title'] == None and data['subject_name'] == None:
            raise serializers.ValidationError("Course Title and Subject Name Cannot be Blank")
        return data
    
#for create LWFAssessment
class LWFAssessmentSerial(serializers.ModelSerializer):
    class Meta:
        model = LWFAssessmentCreateform
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, data):
        title = data.get('title')
        instruction = data.get('instruction')

        if not title and not instruction:
            raise serializers.ValidationError("Title and Instructions cannot be blank")

        return data
    
    
#for create DeadlineManegement
class DeadlineSerial(serializers.ModelSerializer):
    class Meta:
        model = DeadlineManagement
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, data):
        topic = data.get('topic')
        description = data.get('description')

        if not topic and not description:
            raise serializers.ValidationError("Topic and Description cannot be blank")

        return data    
    
       
    

#for live class creation
class ClassSerial(serializers.ModelSerializer):
    class Meta:
        model = ClassCreateform
        fields = '__all__'
    
    def validate(self, data):
        if data['subjectName'] == None and data['joinLink'] == None:
            raise serializers.ValidationError("Subject Name and Joining Link filed Cannot be Blank")
        return data
    
    
class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Show username instead of ID
    assignment = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'submitted_at', 'answer_file', 'status']

    def get_status(self, obj):
        return obj.status()    


 
        