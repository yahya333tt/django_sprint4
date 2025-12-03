from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import SignUp

auth_patterns = [
    path("", include("django.contrib.auth.urls")),
]

urlpatterns = [
    # Можно лучше:
    # Не нужно мешать разные роли модулей! В `urls.py` объявляются маршруты.
    # А настройки контроллеров делаются в модулях `views.py`.
    path("auth/registration/", SignUp.as_view(), name="registration"),
    path("admin/", admin.site.urls),
    path("auth/", include(auth_patterns)),
    # path(
    #     'auth/registration/',
    #     CreateView.as_view(
    #         template_name='registration/registration_form.html',
    #         form_class=BlogUserCreationForm,
    #         success_url=reverse_lazy('blog:index'),
    #     ),
    #     name='registration',
    # ),
    path("pages/", include("pages.urls", namespace="pages")),
    # Можно лучше:
    # Объяснить, что чтобы случайно не затереть стандартные урлы - наши
    # нужно перенести в конец
    # Надо исправить:
    # Урлы приложения blog подключаются именно таким образом и никак иначе.
    # path('', include('blog.urls', namespace='blog')),
    # Реализация ДЗ на функциях вынесена в пакет func_version
    # Для выполнения задания можно использовать view-функции (FBV),
    # view-классы (CBV) или их микс.
    path("", include("blog.func_version.urls", namespace="blog")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "core.views.csrf_failure"
handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
