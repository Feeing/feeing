from django.shortcuts import render
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

