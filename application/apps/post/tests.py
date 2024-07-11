from django.test import TestCase
from .models import Post


class MyTest(TestCase):
    def setUp(self):
        self.my_post = Post
        print(Post.objects.all())

    def test_1(self):
        print(self.my_post)
