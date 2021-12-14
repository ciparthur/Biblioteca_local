from django.contrib import admin
from .models import Livro, Autor, Genero, LivroInstancia

admin.site.register(Livro)
admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(LivroInstancia)
