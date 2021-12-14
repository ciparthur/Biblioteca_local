from django.db import models

class Genero(models.Model):
    """Um modelo que representa o gênero do livro"""
    nome = models.CharField(max_length=200, help_text='Entre com gênero do livro (ex: fantasia).')
    
    def __str__(self):
        """Retorna uma string para representar o modelo"""
        return self.nome
