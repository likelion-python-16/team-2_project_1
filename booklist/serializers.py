from rest_framework import serializers
from .models import Book, Author, Review, Like, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'content', 'rating', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.author', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name',
            'average_rating', 'review_count', 'like_count', 'created_at'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.author', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'author_name',
            'published_at', 'created_at',
            'average_rating', 'review_count', 'like_count',
            'reviews'
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'published_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("제목은 공백일 수 없습니다.")
        if len(value) > 200:
            raise serializers.ValidationError("제목은 200자 이내여야 합니다.")
        return value
    

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def get_book_title(self, obj):
        return obj.book.title
    
    def get_author_name(self, obj):
        return obj.book.author.author