from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import viewsets

from .models import Book
from .serializers import BookSerializer, BookDetailSerializer, BookCreateUpdateSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPageNumberPagination

    # 파일 업로드가 필요하다면 (현재는 사용하지 않음)
    parser_classes = [FormParser, MultiPartParser]

    # 검색 / 정렬 설정
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__author"]
    ordering_fields = ["created_at", "published_at", "review_count", "average_rating"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        return BookCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        # ?min_rating=4.0 같은 필터링 로직 추가 가능
        queryset = Book.objects.all().order_by("-created_at")
        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            queryset = [book for book in queryset if book.average_rating and book.average_rating >= float(min_rating)]
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


# ✅ 세션 로그아웃 API (Axios 기반 또는 Fetch API로 호출)
class CustomLogoutApi(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # Django 내장 세션 종료
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)