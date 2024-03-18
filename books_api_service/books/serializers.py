from rest_framework import serializers
from .models import Books, BookImage


class BooksSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    def get_authors(self, instance):
        # передаем всех авторов, принадлежих к конкртеному экземпляру книги как query set
        authors = instance.authors.all()

        return [author.name for author in authors]  # кладем их имена в список и отдем представлению

    class Meta:
        model = Books
        fields = ['id', 'title', 'isbn', 'pageCount', 'publishedDate', 'thumbnailUrl', 'shortDescription',
                  'longDescription', 'status', 'category_lvl1', 'category_lvl2', 'category_lvl3', 'authors']


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['thumbnailImage', ]
