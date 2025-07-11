from rest_framework import serializers
from .models import Book, Author, Genre, Publisher

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'death_date']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'website', 'contact_email']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genre = GenreSerializer(many=True)
    publisher = PublisherSerializer()
    
    class Meta:
        model = Book
        fields = '__all__'