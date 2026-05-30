from django.contrib.auth import get_user_model
from django.db import models

from core.constants import FIELDS_MAX_LENGTH, STR_LENGTH
from core.models import PublishedAndCreatedAt

User = get_user_model()


# Надо исправить:
# В теории рассказывают про абстрактные модели, так что студенты знают,
# что это и мы требуем от них реализацию.
class Category(PublishedAndCreatedAt):
    # Надо исправить:
    # Все магические числа выносим в константы (не файл settings.py).
    title = models.CharField('Заголовок', max_length=FIELDS_MAX_LENGTH)
    # Надо исправить:
    # Для всех полей нужны verbose_name на русском языке.
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        # Надо исправить:
        # Для полей is_published и slug нужен help_text на русском.
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.',
        unique=True
    )

    # Надо исправить:
    # Не забываем наследовать мету от меты родителя,
    # если у нас есть сортировка в мете родителя.
    class Meta(PublishedAndCreatedAt.Meta):
        # Надо исправить:
        # Для всех моделей нужны verbose_name и verbose_name_plural
        # на русском языке.
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    # Можно лучше:
    # Так как длина этого поля может быть большой, лучше его срезать
    # и так же убрать срез в константу.
    def __str__(self) -> str:
        return self.title[:STR_LENGTH]


class Location(PublishedAndCreatedAt):
    name = models.CharField('Название места', max_length=FIELDS_MAX_LENGTH)

    class Meta(PublishedAndCreatedAt.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:STR_LENGTH]


class Post(PublishedAndCreatedAt):
    title = models.CharField('Заголовок', max_length=FIELDS_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        # Надо исправить:
        # Для поля pub_date нужен help_text на русском.
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        # related_name='posts',
        # Можно лучше:
        # Для автора, местоположения и категории нужно поле связи с
        # постами - related_name.
        # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ForeignKey.related_query_name
    )
    location = models.ForeignKey(
        Location,
        # Надо исправить:
        # По ТЗ это поле не обязательное, поэтому ставим blank=True
        blank=True, null=True,
        # Надо исправить:
        # По ТЗ on_delete должен быть равен SET_NULL
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        # Надо исправить:
        # По ТЗ тут blank=True не нужен.
        Category, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )

    # Надо исправить:
    # Так как у поста, мы переопределяем сортировку, то наследовать
    # мету от родителя не нужно.
    class Meta:
        # Можно лучше:
        # Можно сделать один в мете related_name по умолчанию
        # https://docs.djangoproject.com/en/4.2/ref/models/options/#django.db.models.Options.default_related_name
        # тогда он создастся автоматически для всех полей отношения.
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        # Надо исправить:
        # Убираем сортировку из вью в модель.
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return self.title[:STR_LENGTH]


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'