from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from .serializers import GoogleSocialAuthSerializer
from authentication.serializers import setGoogleAuthenticatedFalse


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
            POST with "auth_token"

            Send An idtoken as from google to get userinfo
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

@api_view()
def logoutGoogleView(request):
    setGoogleAuthenticatedFalse()
    return Response({"message": "Successfully Logged Out Of Google"})