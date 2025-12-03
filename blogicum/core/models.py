from django.db import models


# Можно лучше:
# Выносим из общей абстрактной модели CreatedAt, так как у нас для
# комментариев нет поля публикации, наследуем абстрактную модель ниже от этой,
# чтобы у остальных моделей ничего не поменялось.
class CreatedAt(models.Model):
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("created_at",)


class IsPublishedCreatedAt(CreatedAt):
    is_published = models.BooleanField(
        "Опубликован",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )

    class Meta(CreatedAt.Meta):
        abstract = True
