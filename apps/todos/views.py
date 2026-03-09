from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request: Request) -> Response:
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)