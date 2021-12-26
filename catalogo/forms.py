import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Genero, Autor, Livro

#class RenovacaoLivroModeloFormulario(forms.ModelForm):
#    def clean_devolucao(self):
#        data = self.cleaned_data['devolucao']
        
#        if data < datetime.date.today():
#            raise ValidationError(_('Data inválida - a nova data está no passado.'))

#        if data > datetime.date.today() + datetime.timedelta(weeks=3):
#            raise ValidationError(_('Data inválida - a nova data tem mais de quatro semanas.'))
        
#        return data

    
#    class Meta:
#        model = LivroInstancia
#        fields = ['devolucao']
#        labels = {'devolucao': _('Nova data de devolução')}
#        help_texts = {'devolucao': _('Entre com a nova data de devolução')}


class RenovacaoLivroFormulario(forms.Form):
    """Formulário para renovação de livros"""
    data_renovacao = forms.DateField(label='Data de renovação', help_text='Ensira uma data entre hoje e quatro semanas (padrão é três semanas).')

    def clean_data_renovacao(self):
        data = self.cleaned_data['data_renovacao']
        
        # Verifica se a data não está no passado.
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - a nova data está no passado.'))
        
        # Verifica se a data não está em um futuro distante (mais de quatro semanas)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - a nova data tem mais de quatro semanas.'))
        
        # Lembre-se de sempre retornar os dados limpos
        return data


class CriarAutor(forms.Form):
    """Formulário para o cadastro de novos autores"""
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    preposicao = forms.CharField(label='Preposição', max_length=5, required=False)
    data_nascimento = forms.DateField(label='Data de nascimento')
    data_morte = forms.DateField(label='Morte', required=False)
    
    def clean_nome(self):
        data = self.cleaned_data['nome']
        
        return data
    
    def clean_sobronome(self):
        data = self.cleaned_data['sobrenome']
    
        return data
    
    def clean_preposicao(self):
        data = self.cleaned_data['preposicao']
        
        return data
    
    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        
        return data
    
    def clean_data_morte(self):
        data = self.cleaned_data['data_morte']
        
        return data


class AtualizarAutor(forms.Form):
    """Formulário para alteração do cadastro de autores existentes no banco de dados"""
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    preposicao = forms.CharField(max_length=5, label='Preposição', required=False)
    data_nascimento = forms.DateField(label='Data de nascimento')
    data_morte = forms.DateField(label='Morte', required=False)

    def clean_nome(self):
        data = self.cleaned_data['nome']
        
        return data
    
    def clean_sobrenome(self):
        data = self.cleaned_data['sobrenome']
        
        return data
    
    def clean_preposicao(self):
        data = self.cleaned_data['preposicao']
        
        return data
    
    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        
        return data
    
    def clean_data_morte(self):
        data = self.cleaned_data['data_morte']
        
        return data


class AdicionarLivro(forms.ModelForm):
    #autores = []
    
    #for autor in Autor.objects.all():
        #autores += [(autor.id, autor.nome)]
    
    #titulo = forms.CharField(max_length=200)
    #autor = forms.ChoiceField(choices=autores)
    #sumario = forms.CharField(widget=forms.Textarea, label='Sumário')
    #isbn = forms.CharField(label='ISBN', max_length=13)
    # genero = forms.MultipleChoiceField(label='Gênero', choices=generos)
    
    def clean_data_titulo(self):
        data = self.cleaned_data['titulo']
        
        return data
    
    def clean_data_autor(self):
        data = self.cleaned_data['autor']
        
        return data
    
    def clean_data_sumario(self):
        data = self.cleaned_data['sumario']
        
        return data
    
    def clean_data_isbn(self):
        data = self.cleaned_data['isbn']
        
        return data
    
    def clean_data_genero(self):
        data = self.cleaned_data['genero']
        
        return data


    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'sumario', 'isbn', 'genero']
        labels = {'sumario': _('Sumário'), 'isbn': _('ISBN')}


class EditarLivro(forms.ModelForm):
    pass
