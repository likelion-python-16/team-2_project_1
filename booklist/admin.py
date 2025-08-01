from django.contrib import admin
from .models import Author, Book
from users.models import User

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'author']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'published_at', 'created_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'admin']