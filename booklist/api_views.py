from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets
from .models import Book, Review, Like, Author
from .serializers import BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer, ReviewSerializer, LikeSerializer, AuthorSerializer
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
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPageNumberPagination

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

    def create(self, request, *args, **kwargs):
        import re

        def clean_title(text):
            return re.sub(r'\s+', '', text).lower()

        data = request.data.copy()
        force_create = request.query_params.get("force") == "true"
        force_new_author = data.get("force_new_author") == "true"

        author_name = data.get("author_name", "").strip()
        author_id = data.get("author", "").strip()

            # 1. author_id + author_name 동시 입력 시 오류 반환
        if author_id and author_name:
            return Response(
                {"detail": "⚠️ 저자 선택과 새 저자 입력 중 하나만 작성해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. author 객체 결정
        author = None

        if author_name and force_new_author:
            author = Author.objects.create(author=author_name)
            data["author"] = author.id

        elif author_name and not author_id:
            existing = Author.objects.filter(author__iexact=author_name).order_by("-id")
            if existing.exists():
                author = existing.first()
            else:
                author = Author.objects.create(author=author_name)
            data["author"] = author.id

        elif author_id:
            author = get_object_or_404(Author, id=author_id)
            data["author"] = author.id

        else:
            return Response({"detail": "⚠️ 저자를 선택하거나 새로 입력해주세요."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 3. 중복 도서 검사
        raw_title = data.get("title", "")
        clean_input_title = clean_title(raw_title)
        published_at = data.get("published_at", "").strip()

        if raw_title and published_at and author and not force_create:
            same_books = Book.objects.filter(published_at=published_at, author=author)
            for book in same_books:
                if clean_title(book.title) == clean_input_title:
                    return Response({
                        "detail": (
                            f"⚠️ {published_at}에 출판된 '{author.author}'의 책으로, "
                            f"다음 설명을 가진 책이 이미 있습니다:\n"
                            f"설명: \"{book.description or '설명 없음'}\""
                        )
                    }, status=status.HTTP_400_BAD_REQUEST)

        # 4. 도서 생성
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        author_name = data.get("author_name", "").strip()
        author_id = data.get("author", "").strip()
        force_new_author = data.get("force_new_author") == "true"
        
    # ✅ 1. 새 저자 강제 생성 요청이 있을 경우
        if author_name and force_new_author:
            new_author = Author.objects.create(author=author_name)
            data["author"] = new_author.id

    # ✅ 2. 기존 author_name 처리 로직 (새 저자만 입력한 경우)
        elif author_name and not author_id:
            existing = Author.objects.filter(author__iexact=author_name).order_by("-id")
            if existing.exists():
                data["author"] = existing.first().id
            else:
                new_author = Author.objects.create(author=author_name)
                data["author"] = new_author.id

    # ✅ 3. author_id만 있을 경우는 그대로 둠 (추가로 data["author"] 지정 보장)
        elif author_id:
            data["author"] = author_id

        else:
            return Response({"detail": "⚠️ 저자를 선택하거나 새로 입력해주세요."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 실제 업데이트 실행
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        author = instance.author  # 책 삭제 전에 저자 저장
        self.perform_destroy(instance)

        # 🔄 저자가 더 이상 책을 가지고 있지 않다면 삭제
        if not Book.objects.filter(author=author).exists():
            author.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

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
        user = request.user
        book_id = request.data.get("book")

        if not book_id:
            raise ValidationError("책 ID가 필요합니다.")

        existing_like = Like.objects.filter(user=user, book_id=book_id).first()

        if existing_like:
            # 이미 좋아요 했으면 삭제 (toggle 기능)
            existing_like.delete()
            return Response({"detail": "좋아요 취소됨"}, status=status.HTTP_200_OK)
        else:
            # 좋아요 등록
            serializer = self.get_serializer(data={"book": book_id})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)  # ✅ 여기 필수
            return Response({"detail": "좋아요 등록됨"}, status=status.HTTP_201_CREATED)


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


class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all().order_by("id")
        data = []
        for author in authors:
            books = Book.objects.filter(author=author).values_list("title", flat=True)
            data.append({
                "id": author.id,
                "author": author.author,
                "books": list(books),
            })
        return Response(data)
