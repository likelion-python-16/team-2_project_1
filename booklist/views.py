from rest_framework.views import View
from django.shortcuts import render
from .models import Book, Author
from django.shortcuts import render, redirect, get_object_or_404

# books/
class BookListView(View):
    def get(self, request):
        return render(request, "books/book_list.html")


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        is_liked = book.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
        return render(request, "books/book_detail.html", {"book": book, "is_liked": is_liked})
    

class BookCreateView(View):
    def get(self, request):
        authors = Author.objects.all()
        return render(request, "books/book_create.html", {"authors": authors})
    
    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        published_at = request.POST.get("published_at")
        author_id = request.POST.get("author")
        author_name = request.POST.get("author_name")

        if author_id:
            author = get_object_or_404(Author, pk=author_id)
        elif author_name:
            author, _ = Author.objects.get_or_create(author=author_name)
        else:
            return render(request, "books/book_create.html", {
                "authors": Author.objects.all(),
                "error": "저자를 선택하거나 새로 입력해야 합니다."
            })

        Book.objects.create(
            title=title,
            description=description,
            published_at=published_at,
            author=author
        )
        return redirect("booklist:list")
    

class BookUpdateView(View):
    def get(self, request, id):
        return render(request, "books/book_update.html", {"book_id": id})


# DeleteView - 삭제할 책 정보 확인용
class BookDeleteView(View):
    def get(self, request, id):
        return render(request, "books/book_delete.html", {"book_id": id})
