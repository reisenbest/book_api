from django.contrib import admin
from .models import Books, Author, BookImage


@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ('book', 'thumbnailImage')

    class Meta:
        verbose_name = 'Изображения для книг'
        verbose_name_plural = 'Изображения для книг'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

    class Meta:
        verbose_name = 'Авторы книг'
        verbose_name_plural = 'Авторы книг'


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'publishedDate', 'status',)
    list_filter = ('title', 'publishedDate', 'status',)
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors',)

    class Meta:
        verbose_name = 'Каталог книг'
        verbose_name_plural = 'Каталог книг'
