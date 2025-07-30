# booklist/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet,ReviewViewSet
from .views import BookListView,BookDetailView,BookCreateView

app_name = "booklist"

# API 라우터
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    # API 엔드포인트 (실제 데이터 처리)
    path('api/', include(router.urls)),
    
    # # 페이지 뷰들 (HTML 렌더링)
    # path("", BookListView.as_view(), name="book_list"),                         # /booklist/
    path("list/", BookListView.as_view(), name="list"),                        # 기존 유지  
    path("detail/<int:id>/", BookDetailView.as_view(), name='detail'),
    path("create/", BookCreateView.as_view(), name="create"),             # /booklist/create/
#     path("detail/<int:pk>/", BookDetailView.as_view(), name="book_detail"),    # /booklist/detail/1/

#     path("edit/<int:pk>/", BookEditView.as_view(), name="book_edit"),          # /booklist/edit/1/
]