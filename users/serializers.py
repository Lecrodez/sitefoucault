from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import User


# class UserModel:
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email


# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=20)
#     email = serializers.EmailField()
#
#
# def encode():
#     model = UserModel("Artem", "artem@mail.ru")
#     model_sr = UserSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    roles_id = serializers.IntegerField()
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)