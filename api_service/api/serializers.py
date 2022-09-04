# encoding: utf-8

from rest_framework import serializers

from api.models import UserRequestHistory
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        exclude = ['id', 'user']

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields ="__all__"

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        request = self.context.get('request')
        email =  attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Email / Password is not valid")

        return attrs

    def update(self, instance, validated_data):  # noqa
        pass

    def create(self, validated_data):  # noqa
        pass


class SignInSerializer(serializers.ModelSerializer):
    """ Sign in serializer. """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:  # noqa
        model = User
        fields = '__all__'

    def validate(self, attrs):
        """
        :param dict attrs: Serializer data.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if not password == password2:
            raise serializers.ValidationError("Password does not match")

        return attrs

    def create(self, validated_data):
        """
        :param dict validated_data: Validated serializer data.
        """
        print(validated_data)
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        validated_data.pop('password2')

        return User.objects.create_user(email=email, password=password, **validated_data)