from rest_framework.views import View
from django.shortcuts import render
from .models import Book, Author
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# books/
class BookListView(View):
    def get(self, request):
        return render(request, "books/book_list.html")


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        is_liked = book.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
        return render(request, "books/book_detail.html", {"book": book, "is_liked": is_liked})
    

@method_decorator(staff_member_required(login_url="/users/not_access/"), name='dispatch')
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
    

@method_decorator(staff_member_required(login_url="/users/not_access/"), name='dispatch')
class BookUpdateView(View):
    def get(self, request, id):
        authors = Author.objects.all()
        return render(request, "books/book_update.html", {"book_id": id, "authors": authors})


@method_decorator(staff_member_required(login_url="/users/not_access/"), name='dispatch')
class BookDeleteView(View):
    def get(self, request, id):
        return render(request, "books/book_delete.html", {"book_id": id})
    

class MyPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        liked_books = Book.objects.filter(likes__user=user).distinct()
        reviewed_books = Book.objects.filter(reviews__user=user).distinct()

        return render(request, 'users/mypage.html', {
            'user': user,
            'liked_books': liked_books,
            'reviewed_books': reviewed_books,
            'liked_count': liked_books.count(),
            'reviewed_count': reviewed_books.count(),
        })
