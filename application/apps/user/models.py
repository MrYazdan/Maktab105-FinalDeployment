from django.db import models
from functools import partial
from utils.filename import maker
from apps.user.managers import UserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampMixin, LogicalMixin


class Following(TimeStampMixin):
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="_followings"
    )
    following = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="_followers"
    )
    modify_at = False

    class Meta:
        unique_together = ("follower", "following")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F("following")),
                name="not_prevent_self_follow",
            )
        ]


class User(LogicalMixin, AbstractUser, TimeStampMixin):
    username_validator = RegexValidator(
        r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
    )

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(_("active"), default=False)
    username = models.CharField(
        unique=True, max_length=48, validators=[username_validator]
    )
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=partial(maker, "users", keys=["email"]),
        max_length=255,
        blank=True,
        null=True,
    )

    def follow(self, user):
        Following.objects.get_or_create(
            follower=self,
            following=user,
        )

    @property
    def followers(self):
        return [f.follower for f in self._followers.all()]

    @property
    def followings(self):
        return [f.following for f in self._followings.all()]

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]
