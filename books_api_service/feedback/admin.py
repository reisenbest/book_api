from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'content')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('name', 'email', 'phone_number')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'