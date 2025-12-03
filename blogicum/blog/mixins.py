from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post


# Надо исправить:
# Как минимум требуем такой вариант реализации.
class PostFormMixin(LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        # Можно лучше:
        # post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                "blog:post_detail", post_id=self.kwargs[self.pk_url_kwarg]
            )
        return super().dispatch(request, *args, **kwargs)


# Можно лучше:
# Чтобы не переопределять метод dispatch, так как он слишком уж общий метод,
# чтобы делать в нем эти проверки, можно создать TestAuthorMixin.
# class TestAuthorMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user == self.get_object().author


# Можно лучше:
# Вариант реализации на TestAuthorMixin, без dispatch.
# class PostFormMixin(LoginRequiredMixin, TestAuthorMixin):
#     pk_url_kwarg = 'post_id'
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/create.html'
#
#     def handle_no_permission(self):
#         return redirect('blog:post_detail',
#                         post_id=self.kwargs[self.pk_url_kwarg])
#
#     def get_success_url(self):
#         return reverse('blog:profile',
#                        kwargs={'username': self.request.user.username})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Надо исправить:
#         # Нужно учесть, что для удаления так же нужна форма, чтобы был виден
#         # пост который мы удаляем.
#         context['form'] = PostForm(instance=self.object)
#         return context


# Надо исправить:
# Выносим одинаковый код в mixin, для удаления и редактирования комментариев.
class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"post_id": self.kwargs[self.pk_url_kwarg]}
        )

    def dispatch(self, request, *args, **kwargs):
        # Можно лучше: get_object
        comment = get_object_or_404(
            Comment, pk=self.kwargs[self.pk_url_kwarg]
        )
        if comment.author != self.request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

# Можно лучше:
# Вариант с реализацией проверки автора используя TestAuthorMixin в
# CommentUpdateView и CommentDeleteView.
# class CommentMixin(LoginRequiredMixin):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'blog/comment.html'
#     pk_url_kwarg = 'comment_id'
#
#     def get_success_url(self):
#         return reverse('blog:post_detail',
#                        kwargs={'post_id': self.kwargs['post_id']}
#     )
