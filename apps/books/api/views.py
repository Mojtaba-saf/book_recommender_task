from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.books.api.serializers import BookSerializer, BookSuggestionSerializer
from apps.books.models import Book
from apps.reviews.models import Review


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["genre"]

    def get_queryset(self):
        return Book.objects.all().prefetch_related(
            Prefetch("review_set", queryset=Review.objects.filter(user_id=self.request.user.id)))


class BookGenreSuggestionListAPIView(ListAPIView):
    serializer_class = BookSuggestionSerializer

    def get_queryset(self):
        return Book.objects.raw(
            f"""
            select books.id, books.title, books.author, books.genre, rating as possible_rate
            from books
                     join (select genre, round(avg(rating), 2) as rating
                           from reviews as r
                                    join books as b on r.book_id = b.id
                           where r.user_id = {self.request.user.id}
                           group by genre) genre_level on books.genre = genre_level.genre
            where id not in (select book_id from reviews where user_id = {self.request.user.id})
            order by rating desc, books.genre;
            """
        )


class BookAuthorSuggestionListAPIView(ListAPIView):
    serializer_class = BookSuggestionSerializer

    def get_queryset(self):
        return Book.objects.raw(
            f"""
            select id, title, books.author, genre,author_rating as possible_rating
            from books
                     join (select *
                           from (select round(avg(rating), 2) as author_rating, b.author
                                 from reviews
                                          join books b on b.id = reviews.book_id
                                 where user_id = 1
                                 group by author) as author_scores
                           where author_rating >= 2) author_score on books.author = author_score.author
            where books.id not in (select book_id from reviews where user_id = 1)
            order by author_score.author_rating desc, books.author;
            """
        )
