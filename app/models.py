from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.


class Category(models.Model):
    """For category fields"""

    name = models.CharField(max_length=50, unique=True, verbose_name="Category name")
    published = models.BooleanField(default=True, verbose_name="Is published")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created time")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated time")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"


class Recipe(models.Model):
    """For recipe fields"""

    name = models.CharField(max_length=255, verbose_name="Recipe name")
    content = models.TextField(blank=True, null=True, verbose_name="Recipe content")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created time")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated time")
    published = models.BooleanField(default=True, verbose_name="Is published")
    views_count = models.IntegerField(default=0, verbose_name="Views count")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pk"]


class CustomUser(models.Model):
    """For user profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = models.CharField(max_length=14, blank=True, null=True, verbose_name="Phone")
    mobile = models.CharField(max_length=14, blank=True, null=True, verbose_name="Mobile")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    site = models.URLField(blank=True, null=True, verbose_name="Web site")
    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram with url")
    instagram = models.CharField(max_length=50, blank=True, null=True, verbose_name="Instagram with url")
    facebook = models.CharField(max_length=50, blank=True, null=True, verbose_name="Facebook with url")

    def __str__(self):
        return str(self.user.username)


class Comment(models.Model):
    """For user comments"""

    text = models.TextField()
    post = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment author: {self.commentator}\nComment: {self.text}"

    class Meta:
        ordering = ["-pk"]


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.header}: {self.rating}"
