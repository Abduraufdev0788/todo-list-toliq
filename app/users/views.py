from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserAdminSerializer,
    UserSerializers,
    RegisterSerializers,
    Loginserializers,
    ProfileUpdate,
    ProfileViewSerializers,
    AdminDashboardserializers,
    UserAdminUpdateSerializer,

)

from .permissions import Is_Admin
from .models import CustomUser

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

class Register(APIView):
    def post(self, request:Request)-> Response:
        serializer = RegisterSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            user_json = UserSerializers(user)

            return Response(user_json.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class Login(APIView):
    def post(self,request:Request)->Response:
        serializer = Loginserializers(data = request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = authenticate(username = data['username'], password = data['password'])

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)

                return Response({"token": token.key}, status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class Logout(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self,request:Request)->Response:

        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request:Request)->Response:

        user = request.user

        serializer = UserSerializers(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request:Request)->Response:
        user = request.user

        serializer = ProfileUpdate(data=request.data, partial = True)

        if serializer.is_valid(raise_exception=True):
            updated_user = serializer.update(user, serializer.validated_data)

            serializer = ProfileViewSerializers(updated_user)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request:Request)->Response:
        
        request.user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


class AdminPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Is_Admin]

    def get(self, request:Request)->Response:
        serializer = AdminDashboardserializers({})

        return Response(serializer.data, status=status.HTTP_200_OK)

        
class AdminUserManagment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Is_Admin]

    def get(self, request:Request, pk)->Response:
        user = get_object_or_404(CustomUser, pk = pk)
        serializer = UserAdminSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, pk) -> Response:
        user = get_object_or_404(User, pk=pk)

        serializer = UserAdminUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_user = serializer.update(user, serializer.validated_data)

            user_json = UserAdminSerializer(updated_user)

            return Response(user_json.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            



    













