from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializers(serializers.ModelSerializer):

    confirm = serializers.CharField(max_length = 128)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm', 'is_active']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError("parollar bir xil emas")
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class Loginserializers(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length = 128)


class ProfileUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "roles", "groups", "user_permissions", "is_superuser", "is_staff"]
        extra_kwargs = {
            "username": {
                "required": False
            }
        }

class ProfileViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "roles", "groups", "user_permissions", "last_login", "is_superuser", "is_staff"]


class AdminDashboardserializers(serializers.Serializer):
    total_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_total_users(self, obj):
        return User.objects.count()
    
    def get_users(self, obj):
        return User.objects.all().values(
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', "password", "roles", "groups", "user_permissions"
        ).order_by('-date_joined')
    


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class UserAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'roles', 'is_active', 'is_staff', 'password'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': False},
        }


    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)

        instance.save()

        return instance


