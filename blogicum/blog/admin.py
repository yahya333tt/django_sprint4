from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post, User

admin.site.unregister(User)


# Можно лучше:
# Можно рассказать студентам об админке пользователя, что
# admin.ModelAdmin не подходит для модели User и нужно использовать
# UserAdmin из django.contrib.auth.admin, можно импортировать его
# как as BaseUserAdmin, тогда в ней будут возможности стандартной админки
# пользователя + мы сможем её изменять и выводить свои поля к примеру
# кол-во постов у пользователя.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "posts_count",
    )
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    # Можно рассказать как указать другое поле для ссылки на объект,
    # а не первое в list_display, а то и несколько полей, вдь это перечисление.
    list_display_links = ("username", "id")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name")}),
    )

    # Можно лучше:
    # Для того чтобы изменить описание можно использовать декоратор
    @admin.display(description="Постов у пользователя")
    def posts_count(self, obj):
        return obj.posts.count()


# Можно лучше:
# Можно рассказать о декораторе для регистрации админок.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("text",)
    list_display = (
        "title",
        "author",
        "text",
        "category",
        "pub_date",
        "location",
        "get_image",
        "comments_count",
        "is_published",
    )
    list_editable = ("is_published",)
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"

    # Можно лучше:
    # Можно вывести кол-во комментов в списке постов.
    @admin.display(description="Комментов")
    def comments_count(self, obj):
        return obj.comments.count()

    # Можно лучше:
    # Можно показать картинку.
    @admin.display(description="Картинка")
    def get_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )
        return None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "pk",
        "title",
        "description",
        "slug",
        "is_published",
        "created_at",
    )
    list_editable = ("slug", "is_published")
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("pk", "name", "is_published", "created_at")
    list_editable = ("is_published",)
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


# Надо исправить: Не забываем зарегистрировать админку для комментов.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("post",)
    list_display = ("pk", "post", "author", "text")
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


# Можно лучше:
# Так же можно рассказать, как убрать раздел групп, из админки,
# нужно импортировать её и выполнить следующий код:
admin.site.unregister(Group)

# Можно лучше:
# Можно написать полноценные классы ModelAdmin.

# Надо исправить:
# Все (Category, Location, Post, Comment) модели должны быть зарегистрированы.
