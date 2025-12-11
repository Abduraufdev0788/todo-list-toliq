from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
    
class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed']

    def create(self, validated_data):
        user = self.context['request'].user
        todo = Todo.objects.create(user=user, **validated_data)
        return todo