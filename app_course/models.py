from django.db import models

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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
