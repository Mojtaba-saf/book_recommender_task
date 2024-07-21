from django.db.models import (
    Model,
    CharField,
    UniqueConstraint,
)


class Book(Model):
    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        constraints = [UniqueConstraint(fields=["title", "author", "genre"], name="book_title_author_genre_unique")]

    title = CharField(max_length=50)
    author = CharField(max_length=50)
    genre = CharField(max_length=50)

    def __str__(self):
        return "-".join([self.title, self.genre])
