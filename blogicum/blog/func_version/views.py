from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import PostForm, CommentForm
from blog.models import Category, Post, User, Comment
from users.forms import ProfileUpdateForm

# Можно лучше:
# Выносим все вспомогательные функции в другой файл.
from .services import get_post_or_404, paginate_page, post_annotation
from ..querysets import filter_published_posts


def index(request):
    post_list = paginate_page(
        request, post_annotation(filter_published_posts(Post.objects.all()))
    )
    return render(request, "blog/index.html", context={"page_obj": post_list})


def post_detail(request, post_id):
    post = get_post_or_404(post_id)
    # Надо исправить: неопубликованные посты должен видеть только автор.
    if post.author != request.user:
        post = get_object_or_404(
            filter_published_posts(Post.objects.all()), pk=post_id
        )
    context = {
        "post": post,
        "form": CommentForm(),
        # Можно лучше: Лучше обойтись без лишней одноразовой переменной.
        "comments": post.comments.select_related("author"),
    }
    return render(request, "blog/detail.html", context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = post_annotation(filter_published_posts(category.posts))
    context = {
        "page_obj": paginate_page(request, post_list),
        "category": category,
    }
    return render(request, "blog/category.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = post_annotation(author.posts.all())
    # Надо исправить: неопубликованные посты должен видеть только автор.
    if author != request.user:
        post_list = filter_published_posts(post_list)
    context = {
        "profile": author,
        "page_obj": paginate_page(request, post_list),
    }
    return render(request, "blog/profile.html", context)


@login_required
def edit_profile(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        return redirect("blog:profile", username)
    form = ProfileUpdateForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username)
    return render(request, "blog/user.html", context={"form": form})


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, "blog/create.html", context={"form": form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("blog:profile", request.user.username)


# Можно лучше: Можно вынести повторяющийся из редактирования
# и удаления код в функцию.
# def action_post(request, post_id, is_delete=False):
#     post = get_post_or_404(post_id)
#     if post.author != request.user:
#         return redirect("blog:post_detail", post_id)
#     # Надо исправить: используем or None, вместо лишних условий.
#     form = PostForm(
#         request.POST or None,
#         # Надо исправить: Не забываем добавлять файлы.
#         files=request.FILES or None,
#         instance=post,
#     )
#     if is_delete and request.method == "POST":
#         post.delete()
#         return redirect("blog:profile", request.user.username)
#     if form.is_valid():
#         form.save()
#         return redirect("blog:post_detail", post_id)
#     return render(request, "blog/create.html", context={"form": form})
#
# @login_required
# def post_edit(request, post_id):
#     return action_post(request, post_id)
#
#
# @login_required
# def post_delete(request, post_id):
#     return action_post(request, post_id, is_delete=True)


@login_required
def post_edit(request, post_id):
    post = get_post_or_404(post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id)
    return render(request, "blog/create.html", context={"form": form})


@login_required
def post_delete(request, post_id):
    post = get_post_or_404(post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id)
    form = PostForm(instance=post)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", request.user.username)
    return render(request, "blog/create.html", context={"form": form})


@login_required
def post_create_comment(request, post_id):
    post = get_post_or_404(post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("blog:post_detail", post_id)


# Можно лучше: Можно вынести повторяющийся из редактирования
# и удаления код в функцию.
# def action_comment(request, post_id, comment_id, is_delete=False):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     if comment.author != request.user:
#         return redirect("blog:post_detail", post_id)
#     if is_delete:
#         if request.method == "POST":
#             comment.delete()
#             return redirect("blog:post_detail", post_id)
#         return render(request, "blog/comment.html", {"comment": comment})
#     # Надо исправить: используем or None, вместо лишних условий.
#     form = CommentForm(request.POST or None, instance=comment)
#     if form.is_valid():
#         form.save()
#         return redirect("blog:post_detail", post_id)
#     return render(
#         request,
#         "blog/comment.html",
#         context={"comment": comment, "form": form},
#     )
#
#
# @login_required
# def post_edit_comment(request, post_id, comment_id):
#     return action_comment(request, post_id, comment_id)
#
#
# @login_required
# def post_delete_comment(request, post_id, comment_id):
#     return action_comment(request, post_id, comment_id, is_delete=True)


@login_required
def post_edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id)
    return render(
        request,
        "blog/comment.html",
        context={"comment": comment, "form": form},
    )


@login_required
def post_delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id)
    return render(request, "blog/comment.html", context={"comment": comment})
