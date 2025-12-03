from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Надо исправить: Достаточно эксклюдить тут только автора.
        exclude = ("author",)
        # Надо исправить: Либо удаляем виджет, либо требуем format,
        # чтобы была автоподстановка даты в виджете при редактировании.
        widgets = {
            "pub_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "class": "form-control"},
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        # Можно лучше: Можно писать, можно не писать следующую строку.
        widgets = {"text": forms.Textarea({"cols": "22", "rows": "5"})}
