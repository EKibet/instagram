from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import Profile
# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name="yg")
    title = models.CharField(max_length=60, null=True)
    time_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    likes = models.IntegerField(default=0, null=True)
    caption = models.CharField(max_length=140, default="")
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class Comment(models.Model):
    post = models.ForeignKey('Image', null=True)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey('Image')
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title

class Followers(models.Model):
    user = models.CharField(max_length=20,default='')
    Follower = models.CharField(max_length=20,default='')