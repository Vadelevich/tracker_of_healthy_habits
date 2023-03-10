from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):
        """Переопределим, чтобы хешировался пароль"""
        return User.objects.create(email=validated_data['email'], password=make_password(validated_data['password']),)