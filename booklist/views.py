from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from .models import Book
from .serializers import (
    BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer
)
from .pagination import CustomPageNumberPagination

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

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

    def perform_create(self, serializer):
        serializer.save()

from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class BookViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 생성자 저장