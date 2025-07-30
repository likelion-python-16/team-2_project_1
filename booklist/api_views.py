from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.contrib.auth import logout, login, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import viewsets
from .models import Book
from users.models import User
from .serializers import BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import AllowAny
from django.db.models import Count, Avg



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPageNumberPagination

    # 검색 / 정렬 설정
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__author"]
    ordering_fields = ["created_at", "published_at", "annotated_review_count", "annotated_average_rating"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Book.objects.annotate(
            annotated_review_count=Count("reviews"),
            annotated_average_rating=Avg("reviews__rating")
        ).order_by("-created_at")


    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        return BookCreateUpdateSerializer