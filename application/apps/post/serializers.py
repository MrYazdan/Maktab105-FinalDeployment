from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.post.models import Post, Like, Comment

User = get_user_model()


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "image")
        read_only_fields = ("username", "image")


class PostSerializer(serializers.ModelSerializer):
    author = MinimalUserSerializer(read_only=True)
    likes = serializers.ReadOnlyField(source="likes_count")

    class Meta:
        model = Post
        read_only_fields = ("is_active",)
        exclude = ("is_deleted",)

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class LikesSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Like
        exclude = ("create_at", "post", "id")

    def to_representation(self, instance):
        return super().to_representation(instance)["user"]


class CommentSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        exclude = ("modify_at", "post", "is_deleted", "is_active")
        read_only_fields = ("user",)
        extra_kwargs = {"replies": {"read_only": True}, "reply": {"write_only": True}}

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()
        fields["replies"] = self.__class__(many=True)
        return fields
