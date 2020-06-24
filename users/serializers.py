from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'created_at',
            'updated_at',
        )


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('auth_token', )
        extra_kwargs = {'password': {'write_only': True}}
