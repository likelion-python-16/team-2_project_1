from rest_framework.views import View
from django.shortcuts import render
from .models import Book, Author

# books/
class BookListView(View):
    def get(self, request):
        return render(request, "books/book_list.html")


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        return render(request, "books/book_detail.html", {"book": book})
    

class BookCreateView(View):
    def get(self, request):
        authors = Author.objects.all()
        return render(request, "books/book_create.html", {"authors": authors})
