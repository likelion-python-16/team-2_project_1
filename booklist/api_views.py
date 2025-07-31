from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets
from .models import Book, Review, Like, Author
from .serializers import BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer, ReviewSerializer, LikeSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly
from django.db.models import Count, Avg
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



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
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("이미 이 책에 대한 리뷰를 작성하셨습니다.")
        
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({"detail": "수정 권한 없음"}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if not (request.user.admin or review.user == request.user):
            return Response({"detail": "삭제 권한 없음"}, status=403)
        return super().destroy(request, *args, **kwargs)
        

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        user = request.user

        existing_like = Like.objects.filter(book=book_id, user=user).first()

        if existing_like:
            existing_like.delete()
            return Response({"detail": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
class AuthorBooksAPIView(APIView):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        books = Book.objects.filter(author=author)
        serializer = BookSerializer(books, many=True)

        return Response({
            "author": author.author,
            "book_count": books.count(),
            "books": serializer.data
        }, status=status.HTTP_200_OK)