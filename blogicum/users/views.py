from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import BlogUserCreationForm


class SignUp(CreateView):
    form_class = BlogUserCreationForm
    success_url = reverse_lazy("posts:index")
    template_name = "registration/registration_form.html"
