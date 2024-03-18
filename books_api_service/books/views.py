from books.docs import BookImageView_swagger, BooksFilterView_swagger, BookByISBNView_swagger, \
    SubCategoriesDetailView_swagger, ParseDataView_swagger, CategoriesAndSubCategoriesByLevelView_swagger, \
    BooksListView_swagger, BooksByCategoryView_swagger
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from .filters import BooksFilter
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import CustomPagination
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .utils import add_book_instance_into_db, get_categories_and_sub_categoris_by_lvl
from rest_framework import status
from .models import Books, BookImage
from .serializers import BooksSerializer, BookImageSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class BookImageView(RetrieveAPIView):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
    lookup_field = 'book__isbn'
    permission_classes = [AllowAny]  # повеcил везде здесь ALlowany для удобства, с аутентификацией работает Feedback

    @BookImageView_swagger
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# задания со звездочкой фильтры по дате статусу автору и названию
class BooksFilterView(generics.ListAPIView):
    queryset = Books.objects.all().order_by('title')
    serializer_class = BooksSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BooksFilter
    permission_classes = [AllowAny]  # повеcил везде здесь ALlowany для удобства, с аутентификацией работает Feedback

    @BooksFilterView_swagger
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BooksListView(ListAPIView):
    queryset = Books.objects.all().order_by('title')
    serializer_class = BooksSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # повеcил везде здесь ALlow any для удобства, с аутентификацией работает Feedback

    @BooksListView_swagger
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class BookByISBNView(APIView):
    permission_classes = [AllowAny]

    @BookByISBNView_swagger
    def get(self, request, isbn):
        try:
            book = Books.objects.get(isbn=isbn)
            category = book.category_lvl1

            # Получаем список из 5 случайных книг, находящихся в той же категории
            related_books = Books.objects.filter(category_lvl1=category).exclude(isbn=isbn).order_by('?')[:5]
            # сериализуем запрошенную книгу
            book_serializer = BooksSerializer(book)
            # сериализуем список связанных книг
            related_books_serializer = BooksSerializer(related_books, many=True)

            return Response({
                'Запрашиваемая книга': book_serializer.data,
                '5 случайных книг из той же категории': related_books_serializer.data
            })
        except Books.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)


class BooksByCategoryView(ListAPIView):
    serializer_class = BooksSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # повеcил везде здесь ALlow any для удобства, с аутентификацией работает Feedback

    def get_queryset(self):
        category = self.kwargs['category']
        try:
            books = Books.objects.filter(category_lvl1=category).order_by('title')
            return books
        except Books.DoesNotExist:
            return None

    @BooksByCategoryView_swagger
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Книги в указанной категории не найдены"}, status=status.HTTP_404_NOT_FOUND)


class SubCategoriesDetailView(APIView):
    permission_classes = [AllowAny]  # повеcил везде здесь ALlow any для удобства, с аутентификацией работает Feedback

    @SubCategoriesDetailView_swagger
    def get(self, request, category):
        # находим все записи у которых категория 1 уровня равна переданной и категория 2 уровня не равна null
        books = Books.objects.filter(category_lvl1=category, category_lvl2__isnull=False)

        # проверяем есть ли записи с переданной категорией если нет выкидываем исключение
        if not books.exists():
            return Response({'error': f"Книг у который главная категория {category} нет в базе"},
                            status=status.HTTP_404_NOT_FOUND)

        # создаем пустой словарь и множество в нем для хранения категорий второго уровня
        categories_dict = {category: set()}

        # заполняем словарь под категориями найденными
        for book in books:
            categories_dict[category].add(book.category_lvl2)

        return Response(categories_dict, status=status.HTTP_200_OK)


class ParseDataView(APIView):
    permission_classes = [AllowAny]  # повеcил везде здесь ALlow any для удобства, с аутентификацией работает Feedback

    @ParseDataView_swagger
    def get(self, request):
        url = request.GET.get('url')  # получаем url из параметров запроса
        if not url:
            return Response({'error': 'Требуется ввести utl'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            added_books_count = 0  # счетчик добавленных книг

            # вызываем мейн функцию отвечающую за добавление записей из utils
            # + начинаем счетчки добавленных записей тк при добавлении записи функция возвращает 1
            for book_instance in data:
                if add_book_instance_into_db(book_instance) == 1:
                    added_books_count += 1

            return Response({f'detail': f'В таблицу Books добавлено {added_books_count} записей'},
                            status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': 'Invalid JSON-file'}, status=status.HTTP_400_BAD_REQUEST)


class CategoriesAndSubCategoriesByLevelView(APIView):
    permission_classes = [AllowAny]  # повеcил везде здесь ALlow any для удобства, с аутентификацией работает Feedback

    @CategoriesAndSubCategoriesByLevelView_swagger
    def get(self, request, level: int):
        return get_categories_and_sub_categoris_by_lvl(level)
