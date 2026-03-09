from django.urls import path
from .views import TodoListCreateView

app_name = "todos"

urlpatterns = [
    path("", TodoListCreateView.as_view(), name="todo-list-create"),
]