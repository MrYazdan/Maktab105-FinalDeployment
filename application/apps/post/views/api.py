from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, permissions

from apps.post import serializers
from apps.post.models import Like, Post, Comment
from apps.post.permissions import IsPostAuthorOrReadOnly


class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return Post.objects.filter(
            **({} if self.request.user.is_superuser else {"author": self.request.user})
        ).annotate(likes_count=Count("likes"))


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsPostAuthorOrReadOnly,)
    serializer_class = serializers.PostSerializer

    def get_object(self):
        return get_object_or_404(
            Post.objects.annotate(likes_count=Count("likes")), pk=self.kwargs.get("pk")
        )


class PostLikesListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.LikesSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return post.likes.all().annotate(count=Count("id"))

    def post(self, request, *args, **kwargs):
        user = self.request.user
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        like, like_status = Like.objects.get_or_create(user=user, post=post)

        if not like_status:
            like.delete()

        return response.Response({"status": like_status})


class PostCommentsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("pk"))


class PostCommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.custom
    serializer_class = serializers.CommentSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get("comment_id"))

    # TODO : NOT COMPLETED !!!
