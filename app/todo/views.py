from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


from .serializers import TodoSerializer, TodoCreateSerializer
from ..users.serializers import UserSerializers
from .models import Todo
class TodoListView(APIView):
    authentication_classes = [TokenAuthentication]        

    def post(self, request: Request) -> Response:

        serializer = TodoCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
           todo = serializer.save()
           serializer = TodoSerializer(todo)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: Request) -> Response:
        user = request.user
        search = request.query_params.get('search', None)
        completed = request.query_params.get('completed', None)

        todos = Todo.objects.filter(user = user)
        if search:
            todos = todos.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if completed:
            todos = todos.filter(completed=(completed.lower() == 'true'))
        if completed:
            todos = todos.filter(complated=(completed.lower() == 'false'))
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TodosCrud(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request:Request, pk:int)-> Response:
        user = request.user
        todo = get_object_or_404(Todo, pk = pk)
        user_serializer = UserSerializers(user)
        serializer = TodoSerializer(todo)
        return Response({"user": user_serializer.data, "todo" : serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request:Request, pk:int)-> Response:
        todo = get_object_or_404(Todo, pk = pk)
        serializer = TodoCreateSerializer(todo, data=request.data, context={'request': request})
        user = request.user

        if serializer.is_valid(raise_exception=True):
           todo = serializer.save()
           serializer = TodoSerializer(todo)
           serializer_user = UserSerializers(user)
           return Response({"user": serializer_user.data, "todo": serializer.data}, status=status.HTTP_200_OK)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request:Request, pk:int)->Response:
        todo = get_object_or_404(Todo, pk = pk)

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
