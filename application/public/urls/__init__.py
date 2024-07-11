from public.views import template
from django.urls import path, include

urlpatterns = [
    path("", template.HomeView.as_view(), name="home"),
    path(
        "activate",
        template.generic.TemplateView.as_view(template_name="pages/activate.html"),
        name="public_activate_page",
    ),
    #  /explore
    #  /profile
    #  /notifications
    #
    path("search/", include("public.urls.search")),
]
