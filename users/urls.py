from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # 페이지 URL들
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('not_access/', views.permissionissue.as_view(), name='not_access'),
    
    # API URL들
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
]