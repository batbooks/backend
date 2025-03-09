from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(APIView):
    def get(self, request):
        return Response({'hello': 'world'})
