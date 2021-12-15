from django.shortcuts import render, get_object_or_404
from django.views import generic

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

#def livros(request):
#    """Função view da página de livros"""
#    livros = Livro.objects.all()
#    contexto = {'livros': livros}
    
#    return render(request, 'catalogo/livros_lista.html', contexto)


class LivrosListaView(generic.ListView):
    model = Livro
    context_object_name = 'livros'
    template_name = 'catalogo/livros_lista.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Livro.objects.order_by('titulo')


def livro_detalhes(request, chave_pk):
    """Função view da página de detalhes do livro"""
    livro = get_object_or_404(Livro, pk=chave_pk)
    contexto = {'livro': livro}
    
    return render(request, 'catalogo/livro_detalhes.html', contexto)

#class LivroDetalhe(generic.DetailView):
#    model = Livro
#    context_object_name = 'livro'
#    template_name = 'catalogo/livro_detalhe.html'
