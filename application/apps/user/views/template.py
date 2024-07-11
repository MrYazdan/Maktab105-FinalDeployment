from utils import cache
from django.http import response
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, login

User = get_user_model()


class VerificationView(generic.View):
    template_name = "pages/verify_successful.html"

    def get(self, request, username, token):
        user = get_object_or_404(User, username=username)
        if (
            not (
                token_in_cache := cache.cache.get(
                    f"activate_token_user_{user.username}"
                )
            )
            or token_in_cache != token
        ):
            return response.HttpResponse("Your link has expired!", status=400)

        user.is_active = True
        user.save(update_fields=["is_active"])

        # login:
        login(self.request, user)
        cache.cache.delete(f"activate_token_user_{user.username}")

        return render(request, self.template_name)
