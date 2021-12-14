from django.shortcuts import render

from .models import Livro, LivroInstancia, Autor, Genero

def index(request):
    """Função view do página index do site"""
    
    # Gera contagem de livros e instâncias de livros
    num_livros = Livro.objects.all().count()
    num_instancias = LivroInstancia.objects.all().count()
    num_generos = Genero.objects.all().count()
    
    # Gera contagem de quantos livros estão disponiveis
    num_instancias_disponiveis = LivroInstancia.objects.filter(status__exact='d').count()
    
    num_livros_palavras = Livro.objects.filter(sumario__contains='Deus').count()
    
    # Gera contagem de autores
    num_autores = Autor.objects.count()
    
    contexto = {
        'num_livros': num_livros,
        'num_generos': num_generos,
        'num_instancias': num_instancias,
        'num_instancias_disponiveis': num_instancias_disponiveis,
        'num_autores': num_autores,
        'num_livros_palavras': num_livros_palavras,
    }

    # Renderiza o template 'index.html' com dados na variável de contexto
    return render(request, 'index.html', contexto)
