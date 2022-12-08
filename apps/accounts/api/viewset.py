from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .permissions import IsOwnerOrReadOnly
from apps.accounts.models import *
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegistrationModelSerializer,
    LoginSerializer, ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer, RetrieveModelSerializer
)


class CustomUserCreate(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(username=user_data.get('username'))
        token = RefreshToken.for_user(user)
        if user:
            return Response(str(token.access_token), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class UserPersonalData(RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = RetrieveModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        email = self.request.data['email']
        print(email)
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello \n Use link below to reset your password \n ' + absurl
            data = {
                'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Reset your password'
            }
            print(data)
            Util.send_email(data)

        return Response({'success': 'We have sent you link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(APIView):

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new  one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb': uidb64, 'token': token})

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new  one'})


class SetPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


