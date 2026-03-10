from rest_framework import generics
from rest_framework.permissions import AllowAny

from .filters import TodoFilter, TodoOrdering
from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]
    filterset_class = TodoFilter

    def get_queryset(self):
        queryset = Todo.objects.all()
        queryset = TodoOrdering.apply(
            queryset,
            sort_by=self.request.query_params.get("sort_by"),
            order=self.request.query_params.get("order"),
        )
        return queryset


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]