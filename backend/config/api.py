from rest_framework import routers
from django.urls import path
from apps.users.views import UserViewSet, CheckUserLoginAPIView

# Settings
api = routers.SimpleRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)


urlpatterns = [
    path('check-user-login/', CheckUserLoginAPIView.as_view()),
]

urlpatterns += api.urls
