from django.urls import path
from .views import *

urlpatterns = [
    path('autores' , AutoresView.as_view()),

    ##### GET e POST
    path('authors' , listar_autores),
    path('editoras' , EditoraView.as_view()),
    path('livros', LivroView.as_view()),

    #### UPDATE e DELETE
    path('autor/<int:pk>', AutoresDetailView.as_view()),
    path('editora/<int:pk>', EditoraDetailView.as_view()),
    path('livro/<int:pk>', LivroDetailView.as_view()),

]

