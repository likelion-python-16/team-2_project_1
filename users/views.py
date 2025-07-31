from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserRegistrationSerializer, LoginSerializer
from django.views.generic import TemplateView


# 페이지 뷰들
def login_page(request):
    return render(request, 'users/login.html')

def register_page(request):
    return render(request, 'users/register.html')

# API 뷰들
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'message': '로그인 성공',
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    try:
        logout(request)
        return Response({
            'message': '로그아웃 되었습니다.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': '로그아웃 처리 중 오류가 발생했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

class permissionissue(TemplateView):
    def get(self, request):
        return render(request, 'users/not_access.html')