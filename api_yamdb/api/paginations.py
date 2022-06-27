from rest_framework.pagination import PageNumberPagination


class TitlesPagination(PageNumberPagination):
    page_size = 20


class GenresAndCategoriesPagination(PageNumberPagination):
    page_size = 20
