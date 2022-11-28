from rest_framework import serializers
from apps.accounts.models import *
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed


class RetrieveModelSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(min_length=6, max_length=70, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password', 'confirm']


class RegistrationModelSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=120, required=True, write_only=True)
    email = serializers.CharField(max_length=150, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password', 'confirm']

    def validate(self, attrs):

        password = attrs.get('paasword')
        confirm = attrs.get('confirm')
        username = attrs.get('username')

        user_exist = CustomUser.objects.filter(username=username).first()

        if not (password or confirm) and password != confirm:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match'})

        if user_exist:
            raise serializers.ValidationError('Username exist!')

        return attrs

    def create(self, validated_data):

        phone_number = validated_data['phone_number']
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        hashed_password = make_password(password)

        user = CustomUser(
            username=username,
            password=hashed_password,
            email=email,
            phone_number=phone_number
        )

        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)
    confirm = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        confirm = attrs.get('confirm')

        if password == confirm:

            user_exists = authenticate(requests=self.context.get('request'),
                                       username=username, password=password)

            if not user_exists:
                msg = 'wrong username or password '
                raise serializers.ValidationError(msg, code=status.HTTP_403_FORBIDDEN)

        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code=status.HTTP_400_BAD_REQUEST)

        attrs['user'] = user_exists
        return attrs


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True, write_only=True)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=70, write_only=True)
    confirm = serializers.CharField(
        min_length=6, max_length=70, write_only=True
    )
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm', 'token', 'uidb64']

    def validate(self, attrs):

        try:
            password = attrs.get('password')
            confirm = attrs.get('confirm')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link invalid', 401)

            if password != confirm:
                raise serializers.ValidationError('confirm password does not match', code=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link invalid', 401)
        return super().validate(attrs)
