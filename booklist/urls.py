from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from .api_views import CustomLogoutApi

router = DefaultRouter()
router.register(r'books', BookViewSet)
#URL 경로	설명	name (템플릿용)
# /books/ =  도서 전체 목록 조회	'book-list'
# /books/<pk>/	= 도서 상세 조회	'book-detail'
# /books/	= 도서 생성 (POST)	'book-list'
# /books/<pk>/	= 도서 수정 (PUT/PATCH)	'book-detail'
# /books/<pk>/	= 도서 삭제 (DELETE)	'book-detail'


urlpatterns = [
    path('', include(router.urls)),
    path('logout/', CustomLogoutApi.as_view(), name='logout'),
]