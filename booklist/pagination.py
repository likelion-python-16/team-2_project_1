from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPageNumberPagination(PageNumberPagination):
    """
    커스텀 페이지네이션:
    - page_size 쿼리 파라미터로 페이지 크기 조정 가능
    - page_size=all 이면 전체 데이터 반환
    - 기본 PAGE_SIZE는 settings.py의 REST_FRAMEWORK 설정에서 가져옴
    """
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get("page_size", None)

        if page_size == "all":
            self.page_size = queryset.count()
        else:
            try:
                self.page_size = int(page_size)
            except (TypeError, ValueError):
                self.page_size = self.page_size  # 기본값 유지

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })