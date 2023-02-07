from django.db import models
from django.urls import reverse


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    # verbose_name - для админки задается
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)  # blank=True -
    # необязательное добавление фото из админки blank=True
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True,
                                 verbose_name='Категория', related_name='get_news')  # определяем модель Category как строку, т.к. объявлена
    # Category позже
    views = models.IntegerField(default=0) # кол-во просмотров

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})

    # Null - поле можно не заполнять, default=1 - номер категории для всех записей по умолчанию равна 1
    def __str__(self):  # строковое представление для админки
        return self.title

    class Meta:  # класс для настройки админпанели
        verbose_name = 'Новость'  # наименование модели в единственном числе
        verbose_name_plural = 'Новости'  # наименование модели во множественном числе
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True,
                             verbose_name='Наименование категории')  # db_index индексирует поле

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:  # класс для настройки админпанели
        verbose_name = 'Категория'  # наименование модели в единственном числе
        verbose_name_plural = 'Категории'  # наименование модели во множественном числе
        ordering = ['title']
