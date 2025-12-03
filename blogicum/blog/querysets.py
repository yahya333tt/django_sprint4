from django.db.models import Count, QuerySet
from django.utils.timezone import now


# Надо исправить:
# Выносим аннотацию постов комментариями в функции.
def annotate_posts_comment_count(posts):
    return (
        posts.annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
        .select_related("category", "author", "location")
    )


# Надо исправить:
# Выносим фильтрацию в функции.
def filter_published_posts(posts):
    return posts.filter(
        is_published=True, category__is_published=True, pub_date__lte=now()
    )


# Можно лучше:
# Можно создать свой QuerySet или менеджер моделей.
# https://docs.djangoproject.com/en/3.2/topics/db/managers/#creating-a-manager-with-queryset-methods
class PostQuerySet(QuerySet):
    def annotate_comment_count(self):
        return (
            self.annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
            .select_related("category", "author", "location")
        )

    def filter_published(self):
        return self.filter(
            is_published=True, category__is_published=True, pub_date__lte=now()
        )
