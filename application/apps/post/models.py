from django.db import models
from functools import partial
from utils.filename import maker
from taggit.managers import TaggableManager
from apps.post.managers import CommentManager
from apps.core.managers import LogicalManager
from apps.core.models import TimeStampMixin, LogicalMixin
from django.core.validators import FileExtensionValidator


class Media(TimeStampMixin):
    position = models.PositiveIntegerField(null=False)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="media")
    file = models.FileField(
        upload_to=partial(maker, "posts"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )

    class Meta:
        unique_together = ("post", "position")


class Post(TimeStampMixin, LogicalMixin):
    title = models.CharField(max_length=125)
    author = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.TextField()
    location = models.CharField(max_length=125, null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ("-create_at",)


class Comment(TimeStampMixin, LogicalMixin):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="comments"
    )
    reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()

    objects = CommentManager()
    custom = LogicalManager()

    @property
    def replies(self):
        return self.comment_set(manager="custom")


class Like(TimeStampMixin):
    modify_at = None
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        unique_together = ("post", "user")
        ordering = ("-create_at",)
        indexes = [models.Index(fields=["post", "user"])]
