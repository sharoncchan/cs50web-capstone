from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class User(AbstractUser):
  user_avatar = models.URLField(null=True)
  
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name = "topics")
    title= models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body= models.TextField()
    reading_duration = models.IntegerField()
    image = models.URLField()
    post_date = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name= "likes")
    bookmarks = models.ManyToManyField(User, related_name="bookmarks")
    poster_avatar = models.URLField(null=True)

    def get_absolute_url(self):
        return reverse("post", args=[self.slug])
    


class Comment(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    username = models.ForeignKey(User, on_delete = models.CASCADE,related_name="user_comments")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="post_comments" )
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    comment_avatar = models.URLField(null=True)

    class MPTTMeta:
        order_insertion_by = ["post_date"]

    def __str__(self):
        return f"Comment by {self.username}"



    


