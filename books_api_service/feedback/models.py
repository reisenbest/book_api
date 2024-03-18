from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя',
                             blank=False, help_text='Введите имя')
    email = models.EmailField(verbose_name='Email', max_length=255,  blank=False,
                              help_text='Введите ваш email',)

    content = models.TextField(blank=True, verbose_name='Комментарий',
                                        help_text='Ваш отзыв')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=False,
                                    help_text='Введите номер телефона начиная с +7')

    def __str__(self):
        return self.email
