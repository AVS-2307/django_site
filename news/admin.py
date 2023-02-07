from django.contrib import admin
from django import forms

# Register your models here.
from .models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
    'id', 'title', 'category', 'created_at', 'updated_at', 'is_published')  # поля для отображения в админке
    list_display_links = ('id', 'title')  # поля для отображения как ссылки
    search_fields = ('title', 'content')  # добавление поля поиска
    list_editable = ('is_published',)  # для возможности редактирования поля/полей из админки
    list_filter = ('is_published', 'category',)  # для фильтрации по полю/по полям


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # поля для отображения в админке
    list_display_links = ('id', 'title')  # поля для отображения как ссылки
    search_fields = ('title',)  # добавление поля поиска, это кортеж, не забыть запятую в конце


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
