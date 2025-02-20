from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from users.models import User, Roles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"