from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet, ReviewViewSet, LikeViewSet, AuthorBooksAPIView, AuthorListAPIView
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    MyPageView,
)

app_name = "booklist"

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("api/authors/", AuthorListAPIView.as_view(), name="author-list"),
    path("api/authors/<int:author_id>/books/", AuthorBooksAPIView.as_view(), name="author-books"),

    # 템플릿
    path("list/", BookListView.as_view(), name="list"),
    path("detail/<int:id>/", BookDetailView.as_view(), name='detail'),
    path("create/", BookCreateView.as_view(), name="create"),
    path("update/<int:id>/", BookUpdateView.as_view(), name="update"),
    path("delete/<int:id>/", BookDeleteView.as_view(), name="delete"),

    path("mypage/", MyPageView.as_view(), name="mypage"),  
]