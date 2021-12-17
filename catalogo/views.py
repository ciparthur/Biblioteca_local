from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import generic
# from django.core.paginator import Paginator

from .models import Livro, LivroInstancia, Autor, Genero

def index(request):
    """Função view do página index do site"""
    
    # Gera contagem de livros e instâncias de livros
    num_livros = Livro.objects.all().count()
    num_instancias = LivroInstancia.objects.all().count()
    num_generos = Genero.objects.all().count()
    
    # Gera contagem de quantos livros estão disponiveis
    num_instancias_disponiveis = LivroInstancia.objects.filter(status__exact='d').count()
    
    # Gera contagem de quantas vezes a palavra Deus apareceu em algum sumário dos livros
    num_livros_palavras = Livro.objects.filter(sumario__contains='Deus').count()
    
    # Gera contagem de autores
    num_autores = Autor.objects.count()
    
    # Gera a contagem de visitantes anônimos no site
    num_visitas = request.session.get('num_visitas', 0)
    request.session['num_visitas'] = num_visitas + 1
    
    contexto = {
        'num_livros': num_livros,
        'num_generos': num_generos,
        'num_instancias': num_instancias,
        'num_instancias_disponiveis': num_instancias_disponiveis,
        'num_autores': num_autores,
        'num_livros_palavras': num_livros_palavras,
        'num_visitas': num_visitas,
    }

    # Renderiza o template 'index.html' com dados na variável de contexto
    return render(request, 'index.html', contexto)

def livros(request):
    """Função view da página de livros"""
    try:
        livros = Livro.objects.all().order_by('titulo')
        contexto = {'livros': livros}
    except Livro.DoesNotExist:
        raise Http404('Página não encontrada :(')
    
    # paginator = Paginator(livros, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
        
    return render(request, 'catalogo/livros_lista.html', contexto)

#class LivrosListaView(generic.ListView):
#    model = Livro
#    context_object_name = 'livros'
#    template_name = 'catalogo/livros_lista.html'
#    paginate_by = 10
    
#    def get_queryset(self):
#        return Livro.objects.order_by('titulo')

def livro_detalhes(request, chave_pk):
    """Função view da página de detalhes do livro"""
    livro = get_object_or_404(Livro, pk=chave_pk)
    contexto = {'livro': livro}
    
    return render(request, 'catalogo/livro_detalhes.html', contexto)

def autores(request):
    """Função view para a página de autores dos livros"""
    try:
        autores = Autor.objects.all().order_by('nome')
        contexto = {'autores': autores}
    except Autor.DoesNotExist:
        raise Http404('Página não encontrada :(')

    return render(request, 'catalogo/autores.html', contexto)

def autor_detalhes(request, autor_pk):
    """Função view para a página de detalhes sobre um autor especifico"""
    try:
        autor = Autor.objects.get(pk=autor_pk)
        contexto = {'autor': autor}
    except Autor.DoesNotExist:
        raise Http404('Págnina não encontrada :(')

    return render(request, 'catalogo/autor.html', contexto)
