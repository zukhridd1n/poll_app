from rest_framework.pagination import PageNumberPagination


class ShortedPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 's'
    page_query_param = 'p'

