from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404

from blog.models import Post
from core.constants import POSTS_BY_PAGE


def paginate_page(request, post_list):
    paginator = Paginator(post_list, POSTS_BY_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def post_annotation(obj_list):
    return (
        obj_list.select_related('author', 'location', 'category')
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )


def get_post_or_404(post_id):
    return get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        pk=post_id,
    )