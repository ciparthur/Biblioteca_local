# Generated by Django 4.0 on 2021-12-19 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0005_livroinstancia_mutuaria_alter_autor_preposicao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livroinstancia',
            old_name='mutuaria',
            new_name='mutuario',
        ),
    ]
