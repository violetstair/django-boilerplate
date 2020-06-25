from rest_framework import serializers

from .models import (
    User,
    Profile,
)


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


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'user_id',
            'nickname',
            'bio',
            'address',
            'birthday',
            'gender',
            'phone',
            'created_at',
            'updated_at',
        )


class ProfileCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        profile = Profile.create_profile(validated_data)
        return profile

    def update(self, instance, validated_data):
        profile = Profile.update_profile(instance, validated_data)
        return profile

    class Meta:
        model = Profile
        fields = (
            'user',
            'nickname',
            'bio',
            'address',
            'birthday',
            'gender',
            'phone',
        )

'''
{
  "user": "4b6e6eb6-eea0-4012-a996-e60eb6c1b1bf",
  "nickname": "Roach",
  "bio": "Roach / bridgette.makuch@example.com",
  "address": "국가 도시 지역 동네 1234-1234 1234동 1234층 1234호",
  "birthday": "2007-05-30",
  "gender": "Other",
  "phone": "618-6207-1484"
}
'''