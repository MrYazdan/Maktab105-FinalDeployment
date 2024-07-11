from django.urls import path
from apps.post.views import api

urlpatterns = [
    path("posts", api.PostListCreateAPIView.as_view()),
    path("posts/<pk>", api.PostDetailAPIView.as_view()),
    path("posts/<pk>/likes", api.PostLikesListCreateAPIView.as_view()),
    path("posts/<pk>/comments", api.PostCommentsListCreateAPIView.as_view()),
    path(
        "posts/<int:post_id>/comments/<int:comment_id>",
        api.PostCommentsDetailAPIView.as_view(),
    ),
]
