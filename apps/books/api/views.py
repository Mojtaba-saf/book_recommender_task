from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.books.api.serializers import BookSerializer, BookSuggestionSerializer
from apps.books.models import Book
from apps.reviews.models import Review


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["genre"]

    def get_queryset(self):
        return Book.objects.all().prefetch_related(
            Prefetch(
                "review_set",
                queryset=Review.objects.filter(user_id=self.request.user.id),
            )
        )


class BookSuggestionBaseAPIView(ListAPIView):
    serializer_class = BookSuggestionSerializer

    def get_queryset(self):
        raise NotImplementedError

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "there is not enough data about you"})


class BookGenreSuggestionListAPIView(BookSuggestionBaseAPIView):
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


class BookAuthorSuggestionListAPIView(BookSuggestionBaseAPIView):
    def get_queryset(self):
        return Book.objects.raw(
            f"""
            select id, title, books.author, genre,author_rating as possible_rate
            from books
                     join (select *
                           from (select round(avg(rating), 2) as author_rating, b.author
                                 from reviews
                                          join books b on b.id = reviews.book_id
                                 where user_id = {self.request.user.id}
                                 group by author) as author_scores
                           where author_rating >= 2) author_score on books.author = author_score.author
            where books.id not in (select book_id from reviews where user_id = {self.request.user.id})
            order by author_score.author_rating desc, books.author;
            """
        )


class BookUserSuggestionListAPIView(BookSuggestionBaseAPIView):
    def get_queryset(self):
        return Book.objects.raw(
            f"""
            select id, title, author, book_relation_score.relation_score as possible_rate
            from books
                     join (SELECT book_id, relation_score, rating
                           from reviews
                                    join (select round(avg(abs(t1.rating - t2.rating)), 2) relation_score, t2.user_id
                                          from (select genre, round(avg(rating), 2) as rating
                                                from reviews as r
                                                         join books as b on r.book_id = b.id
                                                where r.user_id = {self.request.user.id}
                                                group by genre) as t1
                                                   join (select user_id, genre, round(avg(rating), 2) as rating
                                                         from reviews as r
                                                                  join books as b on r.book_id = b.id
                                                         group by genre, user_id) as t2 on t1.genre = t2.genre
                                          where t2.user_id != {self.request.user.id}
                                          group by t2.user_id
                                          order by relation_score) as user_score on reviews.user_id = user_score.user_id
                           where reviews.user_id != {self.request.user.id}) as book_relation_score on book_relation_score.book_id = books.id
            order by relation_score, rating desc;
            """
        )
