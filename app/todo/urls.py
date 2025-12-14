from django.urls import path
from .views import TodoListView, TodosCrud


urlpatterns = [
   path("todos/", TodoListView.as_view()),
   path("todos/<int:pk>/", TodosCrud.as_view()),

]
