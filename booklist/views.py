from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Book
from .serializers import (
    BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer
)
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]  # ✅ 한 번만 선언
    pagination_class = CustomPageNumberPagination
    parser_classes = [FormParser, MultiPartParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__author']
    ordering_fields = ['created_at', 'published_at', 'review_count', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        return BookCreateUpdateSerializer

    def get_queryset(self):
        queryset = Book.objects.all().order_by("-created_at")
        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            queryset = [
                book for book in queryset
                if book.average_rating and book.average_rating >= float(min_rating)
            ]
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)