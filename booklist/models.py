from django.db import models
from users.models import User
from django.core.validators import MinValueValidator


class Author(models.Model):
    author = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return f"<작가명: {self.author}>"


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<도서명: {self.title}>"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([review.rating for review in reviews]) / reviews.count(), 1)
        return None

    @property
    def review_count(self):
        return self.reviews.count()
    
    @property
    def like_count(self):
        return self.likes.count()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"<리뷰: {self.user.username} - {self.book.title}>"


class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"<좋아요: {self.user.username} - {self.book.title}>"