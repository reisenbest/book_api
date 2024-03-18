
from .views import ParseDataView, BooksListView, BookByISBNView, BooksByCategoryView, SubCategoriesDetailView, \
    CategoriesAndSubCategoriesByLevelView, BooksFilterView, BookImageView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    # суда передаем через query параметр url адрес по которому находится нужный json для парсинга данных
    path('parsebooks/', ParseDataView.as_view(), name='parse_data'),

    # Получение всех книг.
    path('getbooks/', BooksListView.as_view(), name='books-list'),

    # получение конкретной книги по isbn
    path('getbook/byisbn/<str:isbn>/', BookByISBNView.as_view(), name='book-by-isbn'),

    # Получение всех книг определенной категории
    path('getbooks/bycategory/<str:category>/', BooksByCategoryView.as_view(), name='books_by_category'),

    # получение книг по фильтрам переданным через query параметры
    path('getbooks/byfilter/', BooksFilterView.as_view(), name='filter_books'),

    # Получение подкатегорий по указанной одной категории 1 уровня (на 1 месте)
    path('getsubcategoriesfor/<str:category>/', SubCategoriesDetailView.as_view(), name='categories'),

    # Получение категорий текущего уровня и на 1 ниже.
    path('categories/bylevel/<int:level>/', CategoriesAndSubCategoriesByLevelView.as_view(), name='categories_level'),

    # получение изображения книги по isbn книги
    path('get-image-by-book/<str:book__isbn>/', BookImageView.as_view(), name='book-image'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)