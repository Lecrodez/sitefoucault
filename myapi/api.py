from rest_framework.generics import ListAPIView
from . import serializers
from users import models


# class CategoryListAPIView(ListAPIView):
#     serializer_class = serializers.CategorySerializer
#
#     def get_queryset(self):
#         return models.Category.objects.all()

class UserListAPIView(ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.User.objects.all()


class RolesListAPIView(ListAPIView):
    serializer_class = serializers.RolesSerializers

    def get_queryset(self):
        return models.Roles.objects.all()
