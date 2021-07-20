from rest_framework import serializers
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                'The Token is Invalid Or Expired. Please Login Again'
            )
        if(user_data["aud"] != os.environ.get('GOOGLE_CLIENT_ID')):
            raise AuthenticationFailed(
                'Oops Who Are You?'
            )

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        # import pdb
        # pdb.set_trace()


        return register_social_user(provider=provider,user_id=user_id, email=email, name=name)


