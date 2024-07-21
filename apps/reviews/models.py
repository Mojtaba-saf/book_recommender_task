from django.db.models import Model, ForeignKey, CASCADE, PositiveSmallIntegerField, UniqueConstraint, CheckConstraint, Q

from apps.books.models import Book
from apps.users.models import User


# Create your models here.
class Review(Model):
    class Meta:
        db_table = "reviews"
        constraints = [UniqueConstraint(fields=("book", "user"),name="unique_user_book_review"), CheckConstraint(check=Q(rating__gte=0,rating__lte=5), name="rating_max_min")]

    book = ForeignKey(Book, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    rating = PositiveSmallIntegerField()
