from uuid import uuid4

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from utils import cache, mail
from django.http import response
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from apps.user.tasks import print_after_3s


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(generic.View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = self.request.POST.get("username", None)
        password = self.request.POST.get("password", None)

        if not all((username, password)):
            return response.HttpResponse(
                "'username' or 'password' should not be null !", status=400
            )

        if user := authenticate(password=password, username=username):
            if user.is_active:
                login(self.request, user)
                print_after_3s.delay()

                return redirect("home")

            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 300
            ):
                # send mail !
                mail.send_mail(
                    f"Verification {user.username}",
                    user.email,
                    "mail/verify.html",
                    {
                        "user": user,
                        "token": cache.cache.get(
                            f"activate_token_user_{user.username}"
                        ),
                        "host": self.request.get_host(),
                    },
                )

            return redirect("public_activate_page")

        return response.HttpResponse("User not found !", status=404)
