from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
=======
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, admin=False):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        user = self.model(username=username, email=email, admin=admin)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        return self.create_user(username, email, password, admin=True)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin
>>>>>>> 7f075f50645723c65aecc8b8b2ea5d9746f774c5


class Author(models.Model):
    author = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.author


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='books')
    # on_delete=models.CASCADE ensures that if the user is deleted, their books are also deleted

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([review.rating for review in reviews]) / reviews.count(), 1)
        return None

    @property
    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.book.title}"