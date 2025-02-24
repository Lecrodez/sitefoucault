from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import User, Survey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role_id', 'password']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role_id', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            roles=validated_data['role_id']
        )
        user.set_password(validated_data['password'])  # Хеширование пароля
        user.save()
        return user

#
# class SurveyConstructSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Survey,
#         fields = []
