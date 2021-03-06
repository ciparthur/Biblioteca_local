import datetime

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
# from django.core.paginator import Paginator

from .models import Livro, LivroInstancia, Autor, Genero
from .forms import RenovacaoLivroFormulario, CriarAutor, AtualizarAutor, AdicionarLivro

def index(request):
    """Função view do página index do site"""
    
    livros = Livro.objects.all().order_by('titulo')

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
        'livros': livros,
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

@login_required
def autor_detalhes(request, autor_pk):
    """Função view para a página de detalhes sobre um autor especifico"""
    try:
        autor = Autor.objects.get(pk=autor_pk)
        contexto = {'autor': autor}
    except Autor.DoesNotExist:
        raise Http404('Página não encontrada :(')

    return render(request, 'catalogo/autor.html', contexto)

@login_required
def livros_emprestados(request):
    """Função view para obter uma lista de livros emprestados"""
    try:
        emprestados = LivroInstancia.objects.all().filter(mutuario=request.user).filter(status__exact='e').order_by('devolucao')

        contexto = {'emprestados': emprestados}
    except LivroInstancia.DoesNotExist:
        raise Http404('Página não encontrada :(')

    return render(request, 'catalogo/livros_emprestados.html', contexto)

@login_required
@staff_member_required
@permission_required('catalogo.can_mark_returned')
def mutuarios(request):
    """Função view para obter todos os mutuários para os funcionários"""
    try:
        mutuarios = LivroInstancia.objects.all().filter(status__exact='e').order_by('devolucao')

        contexto = {'mutuarios': mutuarios}

    except LivroInstancia.DoesNotExist:
        raise Http404('Página não encontrada :(')

    return render(request, 'catalogo/mutuarios.html', contexto)

@login_required
@permission_required('catalogo.can_mark_returned')
def renovacao_livro(request, renovacao_pk):
    """Função view para a criação da página de renovação dos livros emprestados"""
    livro_instancia = get_object_or_404(LivroInstancia, pk=renovacao_pk)

    # Se a requisição for POST, então processe os dados do formulário
    if request.method == 'POST':
        # Cria uma instância de formulário e preenche com os dados da requisição (Vinculação)
        formulario = RenovacaoLivroFormulario(request.POST)

        # Verifica se o formulário é válido
        if formulario.is_valid():
            # Processa os dados de 'formulario.cleaned_data conforme for necessário (Aqui apenas gravamos no campo devolução do modelo)
            livro_instancia.devolucao = formulario.cleaned_data['data_renovacao']
            livro_instancia.save()

            # Redireciona para a nova URL
            return HttpResponseRedirect(reverse('mutuarios'))
    # Se o metodo for GET (ou outro metodo) cria um formulário padrão
    else:
        proposta = datetime.date.today() + datetime.timedelta(weeks=3)
        formulario = RenovacaoLivroFormulario(initial={'data_renovacao': proposta})

    contexto = {'formulario': formulario, 'livro_instancia': livro_instancia}

    return render(request, 'catalogo/renovacao_livro.html', contexto)

@login_required
@staff_member_required
def criar_autor(request):
    criar_autor = Autor.objects.all()

    if request.method == 'POST':
        formulario = CriarAutor(request.POST)

        if formulario.is_valid():
            criar_autor = Autor.objects.create()

            criar_autor.nome = formulario.cleaned_data['nome']
            criar_autor.sobrenome = formulario.cleaned_data['sobrenome']
            criar_autor.preposicao = formulario.cleaned_data['preposicao']
            criar_autor.data_nascimento = formulario.cleaned_data['data_nascimento']
            criar_autor.data_morte = formulario.cleaned_data['data_morte']

            criar_autor.save()

            return HttpResponseRedirect(reverse('autores'))
    else:
        formulario = CriarAutor()

    contexto = {'formulario': formulario, 'criar_autor': criar_autor}

    return render(request, 'catalogo/autor_form.html', contexto)

@login_required
@staff_member_required
def alterar_autor(request, alterar_pk):
    autor = Autor.objects.get(pk=alterar_pk)

    if request.method == 'POST':
        formulario = AtualizarAutor(request.POST)

        if formulario.is_valid():
            autor.nome = formulario.cleaned_data['nome']
            autor.sobrenome = formulario.cleaned_data['sobrenome']
            autor.preposicao = formulario.cleaned_data['preposicao']
            autor.data_nascimento = formulario.cleaned_data['data_nascimento']
            autor.data_morte = formulario.cleaned_data['data_morte']

            autor.save()

            return HttpResponseRedirect(reverse('autores'))

    else:
        formulario = AtualizarAutor()

    contexto = {'formulario': formulario, 'autor': autor}

    return render(request, 'catalogo/alterar_autor.html', contexto)

@login_required
@staff_member_required
def deletar_autor(request, deletar_pk):
    autor = Autor.objects.get(pk=deletar_pk)

    if request.method == 'POST':
        autor.delete()

        return HttpResponseRedirect(reverse('autores'))

    contexto = {'autor': autor}    
    return render(request, 'catalogo/autor_confirm_delete.html', contexto)

@login_required
@staff_member_required
def adicionar_livro(request):
    add_livro = Livro.objects.all()
    
    if request.method == 'POST':
        formulario = AdicionarLivro(request.POST)

        if formulario.is_valid():
            add_livro = Livro.objects.create()
            
            add_livro.titulo = formulario.cleaned_data['titulo']
            add_livro.autor = formulario.cleaned_data['autor']
            add_livro.sumario = formulario.cleaned_data['sumario']
            add_livro.isbn = formulario.cleaned_data['isbn']
            add_livro.genero.nome = formulario.cleaned_data['genero']

            add_livro.save()

            return HttpResponseRedirect(reverse('livros'))
    else:
        formulario = AdicionarLivro()
    
    contexto = {'formulario': formulario, 'add_livro': add_livro}

    return render(request, 'catalogo/add_livro.html', contexto)

@login_required
@staff_member_required
def alterar_livro(request):
    pass

@login_required
@staff_member_required
def deletar_livro(request, deletar_pk):
    livro = Livro.objects.get(pk=deletar_pk)
    
    if request.method == 'POST':
        livro.delete()
        
        return HttpResponseRedirect(reverse('livros'))
    
    contexto = {'livro': livro}
    return render(request, 'catalogo/deletar_livro.html', contexto)

def cadastro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        
        if formulario.is_valid():
            novo_usuario = formulario.save()
            
            autenticacao = authenticate(username=novo_usuario.username, password=request.POST['password1'])
            login(request, autenticacao)
            
            return HttpResponseRedirect(reverse('index'))
    else:
        formulario = UserCreationForm()
    
    contexto = {'formulario': formulario}
    
    return render(request, 'registration/cadastro.html', contexto)
