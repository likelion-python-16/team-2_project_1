# from django.contrib import admin
# from .models import Author, Book

# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'author']

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'author', 'published_at', 'created_at']

from django.contrib import admin
from .models import Author, Book
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'book_summary']  # 목록에 책 요약 표시
    readonly_fields = ['book_list_display']
    fields = ['author', 'book_list_display']

    def book_summary(self, obj):
        books = obj.books.order_by('-created_at')
        if not books.exists():
            return "📕 없음"
        titles = [book.title for book in books[:3]]
        text = ", ".join(titles)
        if books.count() > 3:
            text += f" 외 {books.count() - 3}권"
        return text
    book_summary.short_description = "작성한 책 요약"

    def book_list_display(self, obj):
        books = obj.books.order_by('-created_at')
        total = books.count()

        if total == 0:
            return "📕 이 작가의 책이 없습니다."

        display_books = books[:9]
        book_titles = [(book.title,) for book in display_books]

        html = format_html_join('\n', "<li>📘 {}</li>", book_titles)
        if total > 9:
            html += mark_safe(f"<li>📚 외 {total - 9}권 더 있음</li>")
        return mark_safe(f"<ul>{html}</ul>")
    book_list_display.short_description = "작성한 책 목록"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'author_id_display', 'published_at', 'created_at']

    def author_id_display(self, obj):
        return obj.author.id
    author_id_display.short_description = 'Author ID'