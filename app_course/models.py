from django.db import models

from django.conf import settings
from users.models import NULLABLE


class Course(models.Model):
    """Stores a single course"""
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Stores a single course, related to :model:'app_course.Course"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    video = models.URLField(**NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс',
                               related_name='lesson')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    """Stores a single payment, related to :model:'app_course.Course',
     :model:'app_course.Lesson' and :model:'auth.User'"""
    CASH = 'cash'
    BANK_TRANSFER = 'transfer'

    PAYMENT_METHODS = (
        (CASH, 'Наличные'),
        (BANK_TRANSFER, 'Перевод на счет'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Продавец')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный  урок')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.course if self.course else self.lesson}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
