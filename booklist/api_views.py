from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets
from .models import Book, Review
from .serializers import BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer, ReviewSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly
from django.db.models import Count, Avg
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    # queryset = Book.objects.all()
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
    

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("이미 이 책에 대한 리뷰를 작성하셨습니다.")