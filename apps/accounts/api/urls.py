from django.urls import path
from .viewset import LoginView, CustomUserCreate, \
    PasswordTokenCheckAPI, RequestPasswordResetEmail, \
    SetPasswordAPIView, UserPersonalData

urlpatterns = [

    path('', CustomUserCreate.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user-personal-data/<int:pk>', UserPersonalData.as_view(), name='user-personal-data'),
    path('password-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetPasswordAPIView.as_view(), name='password-reset-complete'),
    path('password-reset-complete', SetPasswordAPIView.as_view(), name='password-reset-complete'),

]
