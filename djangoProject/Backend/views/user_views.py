import json

from django.contrib.gis.gdal.libgdal import function
from django.shortcuts import render
from django.db import connection
from Backend.users import users
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from Backend.serializers import UserSerializer,UserSerializerWithToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from djangoProject.Backend import database


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super.validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        request_data = request.body
       # print(request_data)
    request_dict = json.loads(request_data.decode('utf-8'))
    account = request_dict.get('account')
    password = request_dict.get('password')
    type = request_dict.get('type')
    function(database.register,account,password,type)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user,many=False)
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['POST'])
def deleteUser(requset,pk):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)