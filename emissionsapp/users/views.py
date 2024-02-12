# from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import LoginSerializer, UserSerializer

class UserViewSet(viewsets.GenericViewSet):
    """User view set.
    Handle login
    """

    @action(detail=False, methods=["post"])
    def login(self, request):
        """User loging"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserSerializer(user).data,
            "token": token,
        }
        return Response(data, status=status.HTTP_201_CREATED)