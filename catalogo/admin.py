from django.contrib import admin
from .models import Livro, Autor, Genero, LivroInstancia

admin.site.register(Genero)
# admin.site.register(Livro)
# admin.site.register(Autor)
# admin.site.register(LivroInstancia)


class LivroInline(admin.StackedInline):
    model = Livro
    extra = 0
    

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('sobrenome', 'nome', 'data_nascimento', 'data_morte')
    fields = ['sobrenome', 'preposicao', 'nome', ('data_nascimento', 'data_morte')]
    
    inlines = [LivroInline]


class LivroInstanciaInline(admin.StackedInline):
    model = LivroInstancia
    extra = 0

    
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    
    inlines = [LivroInstanciaInline]


@admin.register(LivroInstancia)
class LivroInstancia(admin.ModelAdmin):
    list_display = ('livro', 'status', 'devolucao')
    list_filter = ('status', 'devolucao')
    fieldsets = (
        (None, {
            'fields': ('livro', 'edicao', 'id')
        }),
        
        ('Disponibilidade', {
            'fields': ('status', 'devolucao')
        }),
    )
