########################################################################
from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
#ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, 
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
########################################################################

# Create your views here.

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes=[os.environ.get('APP_SCHEME'),'http', 'https']



class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')



        absUrl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = 'Hi ' +user.username + 'Use Link Below to verify your email\n'+ absUrl
        data = {
            'to_email': user.email,
            'email_subject': 'Verify Your Email',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return CustomRedirect("http://127.0.0.1:8000/email-verified")
        except jwt.ExpiredSignatureError as identifier:
            print(identifier)
            # return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
            return CustomRedirect("http://127.0.0.1:8000/email-verification-failed")
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            # return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return CustomRedirect("http://127.0.0.1:8000/email-verification-failed")




class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(self.request.user.is_authenticated)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return redirect("http://127.0.0.1:8000/")

