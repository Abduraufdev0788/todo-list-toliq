from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from .serializers import TodoSerializer, TodoCreateSerializer

class TodoListView(APIView):
    authentication_classes = [TokenAuthentication]        

    def post(self, request: Request) -> Response:

        serializer = TodoCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
           todo = serializer.save()
           serializer = TodoSerializer(todo)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)