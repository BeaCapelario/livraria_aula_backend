from rest_framework import serializers
from .models import Autor, Editora, Livro

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__' #todos os arquivos

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    editora = EditoraSerializer(read_only=True)
    editora_id = serializers.PrimaryKeyRelatedField(
        queryset = Editora.objects.all(), source ='editora', write_only = True)
    
    autor = AutorSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(
        queryset = Autor.objects.all(), source ='autor', write_only = True)
    
    class Meta:
        model = Livro
        fields = ['id','titulo', 'subtitulo', 'autor', 'autor', 'editora', 'editora', 'isbn', 'descricao', 'idioma', 'ano_publicacao', 'paginas', 'preco', 
                  'estoque', 'desconto', 'disponivel', 'dimensoes', 'peso', 'editora', 'editora_id', 'autor', 'autor_id']

        def __str__(self):
            return self.editora