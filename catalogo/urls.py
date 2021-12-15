from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.LivrosListaView.as_view(), name='livros'),
    path('livros/<int:chave_pk>', views.livro_detalhes, name='livro-detalhes'),
    #path('livros/', views.livros, name='livros'),
    #path('livros/<int:pk>', views.LivroDetalhe.as_view(), name='livro-detalhes'),
]
