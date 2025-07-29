from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    관리자만 수정/삭제 가능. 그 외는 읽기만 허용.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user and request.user.is_authenticated and request.user.admin
        )


class IsOwnerOrAdmin(BasePermission):
    """
    작성자이거나 관리자만 수정/삭제 가능
    """
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user and (
                request.user.admin or obj.user == request.user
            )
        )