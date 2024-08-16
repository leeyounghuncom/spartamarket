from django.db import models
from django.conf import settings


class Hashtag(models.Model):
    content = models.CharField(max_length=50, unique=True)  # 해시태그는 고유해야 함

    def __str__(self):
        return self.content

class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True, default="images/default.png")  # 기본 이미지 설정
    view = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_products", blank=True
    )

    hashtags = models.ManyToManyField(Hashtag, blank=True)


    def __str__(self):
        return self.title

    @property
    def update_counter(self):
        self.view = self.view + 1
        self.save()


class Comment(models.Model):
    article = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updaetd_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


