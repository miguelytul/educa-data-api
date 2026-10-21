from django.shortcuts import render

from rest_framework import generics

from .models import School
from .serializers import SchoolSerializer


class SchoolListView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_fields = ["uf", "municipio"]

# Create your views here.
