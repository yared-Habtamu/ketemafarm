from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}  # Make username optional
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data['role'],
            username=validated_data.get('username')  # Optional
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user

