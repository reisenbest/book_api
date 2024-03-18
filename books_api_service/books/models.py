from django.db import models

'''
есть много вариантов как реализовать хранилище данных

как 1 таблицу, 
как несоклько с авторами и категориями с отношениями many to many

но я не совсем понял ТЗ, а именно часть касающуюся категорий, поэтому исходил из своего понимания
буду рад исправить если будет нужно 
'''


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Авторы',
                             blank=False, help_text='Введите автора', unique=True)

    class Meta:
        verbose_name = "Авторы"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название книги',
                             blank=False, help_text='Введите название книги')
    isbn = models.CharField(max_length=13, verbose_name='Международный стандартный книжный номер',
                            help_text='Введите ISBN', blank=False, unique=True)
    pageCount = models.PositiveIntegerField(verbose_name='Количество страниц',
                                            help_text='Введите количество страниц', blank=False)
    publishedDate = models.DateField(verbose_name='Дата публикации',
                                     help_text='Укажите дату публикации',
                                     blank=True,
                                     null=True)
    thumbnailUrl = models.URLField(verbose_name='Ссылка на миниатюру книги',
                                   help_text='Прикрепите ссылку', blank=False)

    shortDescription = models.TextField(blank=True, verbose_name='Короткое описание',
                                        help_text='Введите короткое описание', default='Отсутствует')
    longDescription = models.TextField(blank=True, verbose_name='Длинное описание',
                                       help_text='Введите длинное описание', default='Отсутствует')
    status = models.CharField(max_length=255, verbose_name='Cтатус книги',
                              blank=False, help_text='Введите статус книги')

    category_lvl1 = models.CharField(max_length=255, verbose_name='Категория 1 уровня',
                                     blank=False, help_text='Введите категорию 1 уровня', default='Новинки')
    category_lvl2 = models.CharField(max_length=255, verbose_name='Подкатегория (категория 2 уровня)',
                                     blank=True, help_text='Введите подкатегорию 2 уровня', null=True)
    category_lvl3 = models.CharField(max_length=255, verbose_name='Подкатегория (категория 3 уровня)',
                                     blank=True, help_text='Введите категорию 3 уровня', null=True)

    authors = models.ManyToManyField(Author)

    class Meta:
        verbose_name = "Каталог книг"
        verbose_name_plural = "Каталог книг"

    def __str__(self):
        return f'{self.title}: isbn - {self.isbn}'


class BookImage(models.Model):
    book = models.OneToOneField(Books, on_delete=models.CASCADE, related_name='image', to_field='isbn')
    thumbnailImage = models.ImageField(upload_to='book_images/', verbose_name='Миниатюра для книги')

    class Meta:
        verbose_name = "Миниатюра для книг"
        verbose_name_plural = "Миниатюра для книг"

    def __str__(self):
        return f'Изображение для книги {self.book}'
