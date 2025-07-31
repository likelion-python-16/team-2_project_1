from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user and request.user.is_authenticated and request.user.admin
        )
    
    # 작성자=삭제하는 사람 조건 삭제
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user and request.user.admin
        )
