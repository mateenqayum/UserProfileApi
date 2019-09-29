from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import permissions
from . import serializers
from . import models
# Create your views here.


class HelloApiView(APIView):
    """
    This is a start api view
    """
    serializer_class = serializers.HelloApiSerializers

    def get(self, request, format=None):
        an_api_view = [
            'Uses HTTP method as function (get, post, patch, put, delete)',
            'It gives you a similar to a traditional Django view',
            'Gives you a the most contorl over your logic',
            'It mapped manually to URLs'
        ]

        return Response({'message': 'Hello World', 'an_api_view': an_api_view})

    def post(self, request):

        serializer = serializers.HelloApiSerializers(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'hello {}'.format(name)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):

        serializer = serializers.HelloApiSerializers(data=request.data)

        return Response({'message', 'Put Method'})

    def patch(self, request, pk=None):
        serializer = serializers.HelloApiSerializers(data=request.data)

        return Response({'message', 'Patch Method'})

    def delete(self, request, pk=None):
        serializer = serializers.HelloApiSerializers(data=request.data)

        return Response({'message', 'Delete Method'})


class HelloViewSet(viewsets.ViewSet):

    """This is the simple viewset"""

    serializer_class = serializers.HelloApiSerializers

    def list(self, request):

        viewset=[
            'Uses action (list, create, update, partial update,)',
            'Automatically maps URLs using routers',
            'Providers more functionality with less Code',
        ]

        return Response({'message': 'Hello!', 'viewset': viewset})

    def retrieve(self, request, pk=None):

        """HTTP GET method"""

        return Response({'HTTP_method': "GET"})

    def create(self, request):

        serializer = serializers.HelloApiSerializers(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'hello {}'.format(name)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        """HTTP update method"""

        return Response({'HTTP_method': "update"})

    def partial_update(self, request, pk=None):

        """HTTP partial update method"""

        return Response({'HTTP_method': "partial_update"})

    def destroy(self, request, pk=None):

        """HTTP Destroy method"""

        return Response({'HTTP_method': "Destroy"})


class UserProfileViewset(viewsets.ModelViewSet):

    """Creating, updating, read user profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """Check emails, name and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        
        """Use the ObtainAuthToken APIView to validate and create a token"""

        return ObtainAuthToken().post(request)


class ProfileFeedItemViewSet(viewsets.ModelViewSet):
    """Handles the feed items for the logged in user """

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfielFeedItemsSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user """

        serializer.save(user_profile=self.request.user)



