from django.shortcuts import render

from rest_framework.views import APIView

from .serializers import TokenSerializer


class TokenView(APIView):
    serializer_class = TokenSerializer
            

