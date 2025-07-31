from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet, ReviewViewSet
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
)

app_name = "booklist"

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    # 템플릿
    path("list/", BookListView.as_view(), name="list"),
    path("detail/<int:id>/", BookDetailView.as_view(), name='detail'),
    path("create/", BookCreateView.as_view(), name="create"),  
]