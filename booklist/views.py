from rest_framework.views import APIView
from django.shortcuts import render

# books/
class BookListView(APIView):
    def get(self, request):
        return render(request, "books/book_list.html")
