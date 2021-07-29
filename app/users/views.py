from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import HttpResponse
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from users.models import User
from users.serializers import UserSerializer


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    basic_auth = False


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def empty_view(request):
    return HttpResponse('')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(ViewSet, APIView):
    serializer_class = AuthTokenSerializer
    permission_classes = []

    def create(self, request):
        return ObtainAuthToken().post(request)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
