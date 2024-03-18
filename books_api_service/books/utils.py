import requests
from django.core.files.base import ContentFile
from django.db import transaction

from .validators import BookValidator
from rest_framework import status
from rest_framework.response import Response
from .models import Books, Author, BookImage


class ConvertField:
    '''
    методы convert_authors_field и convert_categories_field можно объеденить
     в один стандартный но решил оставить так для читамости
    '''

    def __init__(self, book_instance: dict):
        '''

        :param book_instance: принимает экземпляр книги (словарь)
        '''
        self.book_instance = book_instance

    def convert_publishedDate_field(self):
        '''

        :return: удаляет из даты информацию о времени возващает только год месяц и день
        '''
        book_instance = self.book_instance

        if book_instance["status"] == "MEAP":
            return None
        else:
            publishedDate = book_instance['publishedDate']["$date"].split('T')[0]
            return publishedDate

    def convert_authors_field(self):
        '''

        :return: список с авторами книги без пустных значений
        '''

        book_instance = self.book_instance
        authors = book_instance['authors']  # получаем содержмое ключа authors в сыром виде

        clean_authors_list = []  # пустой список
        for author in authors:
            if author:
                clean_authors_list.append(author)  # если не пустая строка добавляем в результирующий список

        return clean_authors_list

    def convert_categories_field(self):
        '''

        :return: список с категориями книги без пустых значений
        '''

        book_instance = self.book_instance
        categories = book_instance['categories']

        clean_categories_list = []
        for category in categories:
            if category:
                clean_categories_list.append(category)

        return clean_categories_list

    def check_image(self):
        '''
        из объекта book_instance передается значение ключа thumbnailUrl (book_instance['thumbnailUrl'])
        если изображение недоступно по тем или иным причинам устанавливаем заглушку для картинки
        :return: при прохождение всех проверок - > true
        '''
        thumbnailUrl = self.book_instance['thumbnailUrl']

        try:
            response = requests.head(thumbnailUrl)
            if response.status_code != 200:
                # Если статус ответа не 200, устанавливаем константное изображение
                self.book_instance[
                    'thumbnailUrl'] = 'https://pamyatniki-izgotovlenie.ru/image/cache/catalog/nashi_raboty/empty[1]-320x320.png'
        except Exception as e:
            # Если произошла ошибка при отправке запроса, также устанавливаем константное изображение
            self.book_instance[
                'thumbnailUrl'] = 'https://pamyatniki-izgotovlenie.ru/image/cache/catalog/nashi_raboty/empty[1]-320x320.png'

        return thumbnailUrl


def save_image_from_url(book_instance, image_url):
    # save_image_from_url(book.isbn, book_instance['thumbnailUrl'])
    try:
        # Отправляем запрос по указанному URL и получаем содержимое изображения
        response = requests.get(image_url)
        response.raise_for_status()  # Проверяем, что запрос выполнен успешно
        image_content = ContentFile(response.content, name=f'{book_instance.isbn}.jpg')
        print('image-content', image_content)
        # Создаем экземпляр книги и сохраняем изображение в поле thumbnail
        book_image = BookImage.objects.create(book=book_instance, thumbnailImage=image_content)
        print('book_imge', book_image)
        print(f"Изображение для книги {book_instance} успешно сохранено.")
        return 1
    except Exception as e:
        # Если произошла ошибка при скачивании или сохранении изображения, обработаем ее
        print(f"Error: {e}")
        return 0


def add_book_instance_into_db(book_instance: dict):
    '''
    аггрегирует в себе методы класса валидации и создает\не создает объект в бд

    :param book_instance: экземпляр одной книги из json файла с книгами
    :return: функция возвращает 1 если книга была добавлена (то есть она валидна и у нее нет дубликатов,
     и 0 если функция отработала, но книга не была добавлена
    '''
    # Создаем экземпляр класса-валидатора для книги
    book_instance_validator = BookValidator(book_instance)

    # Проверяем валидность экземпляра книги в целом по струтуре (наличие ключей необходимых в словаре)
    if not book_instance_validator.book_instance_validate():
        return 0

    # объявляем методы для проверки полей

    validation_methods = [
        book_instance_validator.validate_title,
        book_instance_validator.validate_isbn,
        book_instance_validator.validate_pageCount,
        book_instance_validator.validate_publishedDate,
        book_instance_validator.validate_thumbnailUrl,
        book_instance_validator.validate_status,
        book_instance_validator.validate_authors,
        book_instance_validator.validate_categories
    ]

    # если не все методы отработали как нужно прекращаем выполнение функции
    if not all(method() for method in validation_methods):
        return 0

    # приводим значения даты публикации авторов и категорий к нужному виду
    converter_field = ConvertField(book_instance)

    book_instance['publishedDate'] = converter_field.convert_publishedDate_field()
    book_instance['authors'] = converter_field.convert_authors_field()
    book_instance['categories'] = converter_field.convert_categories_field()
    book_instance['thumbnailUrl'] = converter_field.check_image()

    # обработка поля категории, если пусто = новинки, далее если одна, то она главная, если после нее есть - заполняются
    # создается их список и по номерам внутри этого списка кладутся в бд в соотвествующее поле
    match len(book_instance['categories']):
        case 0:
            book_instance['categories'] = ['Новинки', None, None]
        case 1:
            book_instance['categories'] = [book_instance['categories'][0], None, None]
        case 2:
            book_instance['categories'] = [book_instance['categories'][0], book_instance['categories'][1], None]
        case 3:
            book_instance['categories'] = [book_instance['categories'][0], book_instance['categories'][1],
                                           book_instance['categories'][2]]

    authors_list_for_books_obj = []  # пустой список где будут хранится авторы текущей книги (для добавления в таблицу)

    with transaction.atomic():
        # если проверки выше прошли и книга валидна для добавления в бд -> добавляем ее авторов в таблицу с авторами
        # + создаем список с авторами этой книги чтобы потом привязать авторов к книге
        for author_name in book_instance['authors']:
            author, _ = Author.objects.get_or_create(name=author_name)
            authors_list_for_books_obj.append(author)

        thumbnail_url = book_instance.get('thumbnailUrl', '')
        # если все методы венули True - создаем экземпляр книги если его еще нет.
        # ключевое поле для проверки - isbn - не должно быть двух одинаковых
        # TODO сделать транзакцию with transaction atomic...
        # Создаем экземпляр книги и сохраняем изображение в поле thumbnail
        book, created = Books.objects.get_or_create(
            isbn=book_instance.get('isbn'),
            defaults={
                'title': book_instance.get('title', ''),
                'pageCount': book_instance.get('pageCount', ''),
                'publishedDate': book_instance.get('publishedDate', ''),
                'shortDescription': book_instance.get('shortDescription', ''),
                'longDescription': book_instance.get('longDescription', ''),
                'thumbnailUrl': book_instance.get('thumbnailUrl', ''),
                'status': book_instance.get('status', ''),
                'category_lvl1': book_instance.get('categories', '')[0],
                'category_lvl2': book_instance.get('categories', '')[1],
                'category_lvl3': book_instance.get('categories', '')[2],
            }
        )
        # отладочная информация о добавленных книгах
        if created or not book.authors.exists():
            # добавляем авторов из созданного выще списка в основную -> связываем 2 таблицы.
            book.authors.add(*authors_list_for_books_obj)
            # Сохраняем изображение книги в связанную таблицу
            save_image_from_url(book, book_instance['thumbnailUrl'])

            print(f"Книга {book_instance['title']} добавлена в базу данных")
            print(book_instance['thumbnailUrl'], book.isbn)

            return 1
        else:

            print(f"Книга {book_instance['title']} уже существует в базе данных.")
            print(book_instance['thumbnailUrl'], book.isbn)

            return 0


def get_categories_and_sub_categoris_by_lvl(level: int):
    '''

    :param level: передаем начальный уровнь
    :return: возврашаем категории указанного уровня и категории на урвоень ниже если есть
    '''

    # все уникальные категории указанного уровня
    categories_lvl = Books.objects.values_list(f'category_lvl{level}', flat=True).distinct()

    # пустой словарь для хранения категорий указанного уровня и их подкатегорий
    categories_dict = {}

    # заполняем словарь категориями указанного уровня и их подкатегориями
    for category_lvl in categories_lvl:
        if category_lvl is not None:
            if level == 1:
                # находим все записи, у которых категория указанного уровня равна текущей а нижняя категория не null
                books = Books.objects.filter(category_lvl1=category_lvl, category_lvl2__isnull=False)

                # получаем уникальные подкатегории и кладем их в список
                subcategories = set(book.category_lvl2 for book in books)
                categories_dict[category_lvl] = list(subcategories)

            elif level == 2:

                books = Books.objects.filter(category_lvl2=category_lvl, category_lvl3__isnull=False)

                subcategories = set(book.category_lvl3 for book in books)
                categories_dict[category_lvl] = list(subcategories)

            else:
                categories_dict = {'detail': 'Всего есть только три уровня категория, вы можете указать только 1 или 2'}

    return Response(categories_dict, status=status.HTTP_200_OK)
