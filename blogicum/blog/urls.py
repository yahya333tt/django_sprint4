from django.urls import path

from .views import (
    CategoryListView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    ProfileDetailView,
    ProfileUpdateView,
)

app_name = "blog"


urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path(
        "profile/<str:username>/", ProfileDetailView.as_view(), name="profile"
    ),
    path(
        "profile/<str:username>/edit/",
        ProfileUpdateView.as_view(),
        name="edit_profile",
    ),
    # Можно лучше:
    # Можно вынести одинаковые префиксы (posts, profile) в отдельные списки.
    path("posts/create/", PostCreateView.as_view(), name="create_post"),
    path(
        "posts/<int:post_id>/",
        # Надо исправить:
        # Все ключи и постов и комментов делаем полными - post_id и comment_id
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "posts/<int:post_id>/edit/", PostUpdateView.as_view(), name="edit_post"
    ),
    path(
        "posts/<int:post_id>/delete/",
        PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:post_id>/comment/",
        CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path(
        "category/<slug:category_slug>/",
        CategoryListView.as_view(),
        name="category_posts",
    ),
]
