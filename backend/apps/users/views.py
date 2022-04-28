from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserWriteSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def list(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated and request.user.is_superuser:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def login(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {'message': 'Invalid login'},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=False, methods=['post'])
    def logout(self, request, format=None):
        if request.user.is_authenticated:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def password_reset(self, request, format=None):
        if User.objects.filter(email=request.data['email']).exists():
            user = User.objects.get(email=request.data['email'])
            params = {'user': user, 'DOMAIN': settings.DOMAIN}
            send_mail(
                subject='Password reset',
                message=render_to_string('mail/password_reset.txt', params),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.data['email']],
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def password_change(self, request, format=None):
        if User.objects.filter(token=request.data['token']).exists():
            user = User.objects.get(token=request.data['token'])
            user.set_password(request.data['password'])
            user.token = uuid4()
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CheckUserLoginAPIView(APIView):

    def get(self, request, format=None):
        is_logged_in = self.request.user.is_authenticated
        if is_logged_in:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
