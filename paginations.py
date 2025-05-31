from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlparse, urlunparse


class CustomPagination(PageNumberPagination):
    def adjust_scheme(self, url):
        if url:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if hostname not in ['127.0.0.1', 'localhost']:
                parsed = parsed._replace(scheme='https')
                return urlunparse(parsed)
        return url

    def get_next_link(self):
        url = super().get_next_link()
        return self.adjust_scheme(url)

    def get_previous_link(self):
        url = super().get_previous_link()
        return self.adjust_scheme(url)

    def get_paginated_response(self, data):

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
