from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.livros, name='livros'),
    path('livros/<int:chave_pk>', views.livro_detalhes, name='livro-detalhes'),
    path('autores/', views.autores, name='autores'),
    path('autores/<int:autor_pk>', views.autor_detalhes, name='autor-detalhes'),
    path('meus_livros', views.livros_emprestados, name='livros-emprestados'),
    path('mutuarios/', views.mutuarios, name='mutuarios'),
    path('livro/<uuid:renovacao_pk>/renovacao/', views.renovacao_livro, name='renovacao-livro'),
    path('autor/criar/', views.criar_autor, name='criar-autor'),
]
