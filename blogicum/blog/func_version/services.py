from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post, Comment
from core.constants import POSTS_BY_PAGE


# Надо исправить:
# Выносим pagination в отдельную функцию.
def paginate_page(request, post_list):
    paginator = Paginator(post_list, POSTS_BY_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


# Надо исправить:
# Выносим аннотацию и выборку в отдельную функцию, так как она нужна
# в нескольких местах.
def post_annotation(obj_list):
    return (
        obj_list.select_related("author", "location", "category")
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )


# Надо исправить:
# Так как нам нужно 5 раз получать пост, то лучше вынести получение
# поста в функцию.
def get_post_or_404(post_id):
    return get_object_or_404(
        Post.objects.select_related("author", "location", "category"),
        pk=post_id,
    )
