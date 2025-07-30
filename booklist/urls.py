from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet
from .views import (
    BookListView,
)

app_name = "booklist"

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    # 템플릿
    path("list/", BookListView.as_view(), name="list"),
]