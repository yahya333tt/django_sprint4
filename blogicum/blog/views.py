from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)

from core.constants import POSTS_BY_PAGE
from users.forms import ProfileUpdateForm
from .forms import CommentForm, PostForm
from .mixins import (
    CommentMixin,
    # TestAuthorMixin,
    PostFormMixin,
)
from .models import Category, Post, User, Comment
from .querysets import annotate_posts_comment_count, filter_published_posts


# Можно лучше:
# Так как у нас одиночный объект (профайл) для фильтрации списка
# объектов (постов)
# https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/#using-singleobjectmixin-with-listview
class ProfileDetailView(ListView):
    model = User
    template_name = "blog/profile.html"
    context_object_name = "profile"
    # Надо исправить:
    # Там где есть метод get_queryset, pagination можно не писать, просто
    # указать в теле класса paginate_by.
    paginate_by = POSTS_BY_PAGE

    def get_profile(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        author = self.get_profile()
        posts = annotate_posts_comment_count(author.posts)
        # Можно лучше:
        # posts = author.posts.annotate_comment_count()
        # Надо исправить:
        # Только автор должен видеть не опубликованные посты.
        if author != self.request.user:
            posts = filter_published_posts(posts)
            # Можно лучше:
            # posts = posts.filter_published()
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        return context

    # Можно лучше:
    # def get_context_data(self, **kwargs):
    #     return {**super().get_context_data(**kwargs),
    #             'profile': self.get_profile()}


# Надо исправить:
# Используем LoginRequiredMixin, для проверки авторизации.
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    slug_url_kwarg = "username"
    model = User
    form_class = ProfileUpdateForm
    template_name = "blog/user.html"

    # Надо исправить:
    # get_object должен выглядеть именно так:
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        # Надо исправить: Используем обычный reverse, reverse_lazy тут не нужен
        return reverse(
            "blog:profile",
            # Надо исправить:
            # Обязательно используем атрибут self.slug_url_kwarg
            kwargs={"username": self.kwargs[self.slug_url_kwarg]},
        )


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = POSTS_BY_PAGE

    def get_queryset(self):
        # Надо исправить:
        # Аннотируем посты кол-вом комментариев и добавляем select_related.
        return annotate_posts_comment_count(
            filter_published_posts(Post.objects)
        )
        # Можно лучше:
        # return Post.objects.filter_published().annotate_comment_count()


class PostCreateView(LoginRequiredMixin, CreateView):
    # Можно лучше: необязательное поле.
    # pk_url_kwarg = 'post_id'
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    # Надо исправить: Достаточно двух методов ниже.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile",
            # Надо исправить: Строго необходимо передавать
            # именно username, а не просто user.
            kwargs={"username": self.request.user.username},
        )


class PostDetailView(DetailView):
    pk_url_kwarg = "post_id"
    model = Post
    template_name = "blog/detail.html"

    # Надо исправить: сигнатура метод get_object должна совпадать с
    # сигнатурой родителя.
    # Вариантов правильного решения тут несколько:
    def get_object(self, queryset=None):
        # Надо исправить: Используем self.pk_url_kwarg
        post = get_object_or_404(self.model, id=self.kwargs[self.pk_url_kwarg])
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            filter_published_posts(self.get_queryset()),
            id=self.kwargs[self.pk_url_kwarg],
        )

    # Еще один вариант:
    # def get_object(self, queryset=None):
    #     post = super().get_object()
    #     if post.author == self.request.user:
    #         return post
    #     return super().get_object(
    #         filter_published_posts(self.get_queryset())
    #     )

    # Еще один вариант:
    # def get_queryset(self):
    #     post = get_object_or_404(Post, id=self.kwargs['post_id'])
    #     return (Post.objects.all() if post.author == self.request.user
    #             else filter_published_posts(Post.objects.all()))

    # Еще один вариант (Можно лучше):
    # def get_object(self, queryset=None):
    #     post = get_object_or_404(self.model, id=self.kwargs[self.pk_url_kwarg])
    #     if (
    #         post.author == self.request.user
    #         or post.is_published and post.pub_date <= now() and post.category.is_published
    #     ):
    #         return post
    #     raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.get_object().comments.select_related(
            "author"
        )
        return context


class PostUpdateView(PostFormMixin, UpdateView):
    # Можно лучше:
    # Можно перенаправить пользователя после редактирования не на профайл,
    # а на пост.
    def get_success_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={"post_id": self.kwargs[self.pk_url_kwarg]},
        )


# Вариант реализации на TestAuthorMixin, без dispatch.
# class PostUpdateView(PostFormMixin, UpdateView):
#     Можно лучше:
#     Можно перенаправить пользователя после редактирования не на профайл,
#     а на пост.
#     def get_success_url(self):
#         return reverse('blog:post_detail',
#                        kwargs={'post_id': self.kwargs[self.pk_url_kwarg]})


class PostDeleteView(PostFormMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Надо исправить:
        # Нужно учесть, что для удаления нужна форма, чтобы был виден
        # пост который мы удаляем.
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


# Вариант реализации на TestAuthorMixin, без dispatch.
# class PostDeleteView(PostFormMixin, DeleteView):
#     Надо исправить:
#     Нужно учесть, что для удаления нужна форма, чтобы был виден
#     пост который мы удаляем.
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = PostForm(instance=self.object)
#         return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            filter_published_posts(Post.objects), id=self.kwargs["post_id"]
        )
        return super().form_valid(form)


class CommentUpdateView(CommentMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, DeleteView):
    pass


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category.html"
    paginate_by = POSTS_BY_PAGE

    def get_category(self):
        return get_object_or_404(
            Category, is_published=True, slug=self.kwargs["category_slug"]
        )

    def get_queryset(self):
        return annotate_posts_comment_count(
            filter_published_posts(self.get_category().posts)
        )
        # Можно лучше:
        # return (self.get_category().posts.
        #         annotate_comment_count().
        #         filter_published())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context
