# from django.forms import model_to_dict
# from django.shortcuts import render, redirect
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import generics
#
# # from .models import User
# from .serializers import UserSerializer
#
#
# # class UserAPIView(generics.ListAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
#
# class UserAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user_new = User.objects.create(
#             first_name=request.data['first_name'],
#             last_name=request.data['last_name'],
#             email=request.data['email'],
#             roles_id=request.data['roles_id'],
#         )
#         return Response({'user': UserSerializer(user_new).data})
#
#     def get(self, request):
#         w = User.objects.all()
#         return Response({'users': UserSerializer(w, many=True).data})
