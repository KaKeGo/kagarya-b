from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.request.build_absolute_uri('?page=1'),
                'last': self.request.build_absolute_uri(f'?page={self.page.paginator.num_pages}'),
            },
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
