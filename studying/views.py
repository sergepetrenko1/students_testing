from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from .models import Testing, MatchTask
from .serializers import TestingSerializer, MatchSerializer
# Create your views here.


class TestingView(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer


class MatchView(viewsets.ModelViewSet):
    queryset = MatchTask.objects.all()
    serializer_class = MatchSerializer
