# accounts/models.py

from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_profiles', blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='default_profile.png')

    def __str__(self):
        return self.user.username

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.user.following_profiles.count()