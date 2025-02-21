from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import User, Roles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        ref_name = 'MyUser Serializer'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'roles', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            roles=validated_data['roles']
        )
        user.set_password(validated_data['password'])  # Хеширование пароля
        user.save()
        return user


class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"