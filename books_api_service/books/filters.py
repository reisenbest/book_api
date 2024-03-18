import django_filters
from django_filters import rest_framework as filters
from .models import Books


class BooksFilter(filters.FilterSet):
    '''
         создаем кастомный фильтр чтобы изменить фильтрацию по авторам
         в стоковом варианте принимает id тк связь many-to-many
         также добавляем функциональности датировкам по дате
        '''

    authors = django_filters.CharFilter(field_name='authors__name', lookup_expr='contains',
                                        label='Авторы')
    title = django_filters.CharFilter(lookup_expr='icontains')
    publishedDate = filters.DateFromToRangeFilter(
        field_name='publishedDate',
        help_text="Фильтрация по диапазону дат публикации книги."
                  "&publishedDate_after=YYYY-MM-DD&publishedDate_before=YYYY-MM-DD"

    )

    class Meta:
        model = Books
        fields = ['title', 'status', 'authors', 'publishedDate']
