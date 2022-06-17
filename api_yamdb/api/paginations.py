from rest_framework.pagination import PageNumberPagination


class CategoriesPagination(PageNumberPagination):
    page_size = 20


class TitlesPagination(PageNumberPagination):
    page_size = 20


class GenresPagination(PageNumberPagination):
    page_size = 20