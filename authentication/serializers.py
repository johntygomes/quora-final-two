from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from main.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

MAIN_USER_IS_AUTHENTICATED = False
MAIN_USER_ID = None
MAIN_USER_NAME = None 
GOOGLE_AUTHENTICATED = True

def setAuthenticationFalse():
    global MAIN_USER_IS_AUTHENTICATED
    MAIN_USER_IS_AUTHENTICATED = False
    global MAIN_USER_ID
    MAIN_USER_ID = None
def setAuthenticationTrue(user_id):
    global MAIN_USER_IS_AUTHENTICATED
    MAIN_USER_IS_AUTHENTICATED = True
    global MAIN_USER_ID
    MAIN_USER_ID = user_id
def setGoogleAuthenticatedTrue():
    global GOOGLE_AUTHENTICATED
    GOOGLE_AUTHENTICATED = True
def setGoogleAuthenticatedFalse():
    global GOOGLE_AUTHENTICATED
    GOOGLE_AUTHENTICATED = False

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)            

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)    
    username = serializers.CharField(max_length=255, min_length=3,read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }


    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']   


    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        # print(user.is_authenticated)
        if filtered_user_by_email:
            if filtered_user_by_email[0].auth_provider != 'email':
                raise AuthenticationFailed("please login using "+ filtered_user_by_email[0].auth_provider)
            # import pdb 
            # pdb.set_trace()
        if not user:
            raise AuthenticationFailed("Invalid Credentials Try Again")
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled,contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('email not verified')
        global MAIN_USER_IS_AUTHENTICATED
        global MAIN_USER_ID
        MAIN_USER_IS_AUTHENTICATED = True
        MAIN_USER_ID = user.id
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
        }

        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('token expered or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # RefreshToken(self.token).blacklist()
            global MAIN_USER_IS_AUTHENTICATED
            global MAIN_USER_ID
            MAIN_USER_IS_AUTHENTICATED=False
            MAIN_USER_ID=None
        except TokenError:
            self.fail('bad_token')