from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    관리자(admin)만 수정/삭제 가능하고,
    나머지 사용자는 읽기(GET, HEAD, OPTIONS)만 가능.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            (request.user and request.user.admin)
        )


class IsOwnerOrAdmin(BasePermission):
    """
    객체 작성자(user) 또는 관리자(staff)만 수정/삭제 가능.
    읽기 요청(GET, HEAD, OPTIONS)은 모두 허용.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff