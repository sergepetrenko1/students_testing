from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Student, Test
from .serializers import TestSerializer, StudSerializer


class StudView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudSerializer
