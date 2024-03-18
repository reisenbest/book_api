from books.serializers import BooksSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

BookImageView_swagger = swagger_auto_schema(
    operation_description="Получения изображения книги по ее isbn",
    operation_summary="Получения изображения книги по ее isbn",
    tags=["Books endpoints"],
    responses={
        200: "OK - Successful response",
        404: "Not Found - Book image with the specified ISBN does not exist",
    }
)

BooksListView_swagger = swagger_auto_schema(
    operation_summary="Список всех книг",
    operation_description="Возвращает список всех книг в базе данных.",
    responses={200: BooksSerializer(many=True)},
    tags=["Books endpoints"],
)

BooksByCategoryView_swagger = swagger_auto_schema(
    operation_summary="Список книг в указанной категории",
    operation_description="Возвращает список всех книг в указанной категории.",
    responses={200: BooksSerializer(many=True), 404: "Книги в указанной категории не найдены"},
    tags=["Books"],
)

BooksFilterView_swagger = swagger_auto_schema(
    operation_summary="Получение списка книг c возможностью фильтрации по дате, автору, статусу, названию",
    operation_description="Получение списка книг c возможностью фильтрации по дате, автору, статусу, названию",
    responses={200: BooksSerializer(many=True)},
    tags=["Books endpoints"],
    manual_parameters=[
        openapi.Parameter(
            name='title',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Поиск по названию книги (по частичному совпадению)',
        ),
        openapi.Parameter(
            name='status',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Фильтр по статусу книги PUBLISH|MEAP',
        ),
        openapi.Parameter(
            name='authors',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Поиск по автору книги (по частичному совпадению)',
        ),
        openapi.Parameter(
            name='publishedDate',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Фильтр по дате публикации книги. В формате '
                        '&publishedDate_after=YYYY-MM-DD&publishedDate_before=YYYY-MM-DD',
        ),
    ],
)

BookByISBNView_swagger = swagger_auto_schema(
    operation_summary="Получение книги по ISBN + 5 случайных книг из той же категории что и запрашиваемая",
    tags=["Books endpoints"],
    manual_parameters=[
        openapi.Parameter(
            'isbn',
            openapi.IN_PATH,
            description="Книга, которая соответствует переданному isbn",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: openapi.Response("Книга, которая соответствует переданному isbn + "
                                     "5 случайных книг из той же категории что и запрашиваемая",
                                     BooksSerializer(many=False))},
)

SubCategoriesDetailView_swagger = swagger_auto_schema(
    operation_summary="Получение подкатегорий по указанной категории 1 уровня (на 1 месте)",
    operation_description="Возвращает подкатегории словарь, где ключ - указанная категория, значение - список ее подкатегорий",
    tags=["Categories endpoints"],
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Категория 1 уровня': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description='Ее подкатегории'
            )
        }
    )}
)

ParseDataView_swagger = swagger_auto_schema(
    operation_summary="Добавление данных из json по указанному url",
    tags=["Parse data from json endpoints"],
    manual_parameters=[
        openapi.Parameter(
            'url',
            openapi.IN_QUERY,
            description="url, по которому доступен json с данными",
            type=openapi.TYPE_STRING
        )
    ]
)

CategoriesAndSubCategoriesByLevelView_swagger = swagger_auto_schema(
    operation_summary="Получение ВСЕХ категорий текущего уровня и на 1 ниже",
    operation_description="Возвращает словарь, где ключи - категории текущего (указаного в параметрах) уровня, "
                          "а значения - список подкатегорий (категорий на уровень ниже) "
                          "либо пустой список если таких нет .",
    tags=["Categories endpoints"],
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_lvl': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description='Подкатегории текущего (указаного в параметрах) уровня'
            )
        }
    )}
)
