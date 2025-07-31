from rest_framework.views import View
from django.shortcuts import render
from .models import Book, Review


# books/
class BookListView(View):
    def get(self, request):
        return render(request, "books/book_list.html")


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        reviews = Review.objects.filter(book=book)
        return render(request, "books/book_detail.html", {"book": book, "reviews": reviews})
    
class BookCreateView(View):
    def get(self, request):
        return render(request, "books/book_create.html")
    
