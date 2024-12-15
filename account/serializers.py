from rest_framework import serializers
from django.contrib.auth.models import User
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email','password','password2']
    
    #p & p are same
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password and Confirm Password must be same")
        return data 
    
    #  encrypt pass
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data['email'],
            password=validated_data['password'],
        )
        return user
        