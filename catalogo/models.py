from django.db import models
from django.urls import reverse
import uuid

class Genero(models.Model):
    """Um modelo que representa o gênero do livro"""
    nome = models.CharField(max_length=200, help_text='Entre com gênero do livro (ex: fantasia).')
    
    class Meta:
        verbose_name = 'Gênero'
    
    def __str__(self):
        """Retorna uma string para representar o modelo"""
        return self.nome


class Livro(models.Model):
    """Um modelo que representa um livro"""
    titulo = models.CharField(max_length=200, help_text='Entre com o título do livro.')
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    sumario = models.TextField('Sumário', max_length=1000, help_text='Entre com uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=11, help_text='Número <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a> de 13 caracteres')
    genero = models.ManyToManyField(Genero, verbose_name='Gênero', help_text='Selecione um gênero para o livro.')
    
    def __str__(self):
        """Retorna uma string para representar o modelo"""
        return self.titulo

    def get_absolute_url(self):
        """Retorna um url para um acesso particular a instância livro"""
        return reverse("livro-detail", args=[str(self.id)])

    def display_genero(self):
        """Cria uma string para o gênero. Isso é necessário para o dislay genero no site Admin"""
        return ', '.join(genero.nome for genero in self.genero.all()[:3])
    
    display_genero.short_description = 'Gênero'


class LivroInstancia(models.Model):
    """Um modelo que representa uma cópia do livro em específico"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para este livro específico em toda a biblioteca')
    livro = models.ForeignKey('Livro', on_delete=models.SET_NULL, null=True)
    edicao = models.CharField('Edição', max_length=200)
    idioma = models.CharField(max_length=20, blank=True, default='Português')
    devolucao = models.DateField('Devolução', null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Em manutenção'),
        ('e', 'Em empréstimo'),
        ('d', 'Disponível'),
        ('r', 'Reservado')
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro'
    )
    
    class Meta:
        ordering = ['devolucao']
        verbose_name_plural = 'Instâncias de livros'

    
    def __str__(self):
        """Retorna um string para representar o modelo"""
        return f'{self.id} {self.livro.titulo}'


class Autor(models.Model):
    """Um modelo que representa um autor"""
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    preposicao = models.CharField(max_length=5, null=True, blank=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    data_morte = models.DateField('Morte', null=True, blank=True)
    
    class Meta:
        ordering = ['sobrenome', 'nome']
        verbose_name_plural = 'Autores'
    
    def get_absolute_url(self):
        """Retorna uma url para acesso particular a instância autor"""
        return reverse("autor-detail", args=[str(self.id)])
        
    def __str__(self):
        """Retorna um string para representar o modelo"""
        return f'{self.sobrenome}, {self.nome}'
