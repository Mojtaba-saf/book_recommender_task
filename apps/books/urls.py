from django.urls import path

from apps.books.api.views import (
    BookListAPIView,
    BookGenreSuggestionListAPIView,
    BookAuthorSuggestionListAPIView,
    BookUserSuggestionListAPIView,
)

urlpatterns = [
    path("books", BookListAPIView.as_view()),
    path("books/suggestion/genre", BookGenreSuggestionListAPIView.as_view()),
    path("books/suggestion/author", BookAuthorSuggestionListAPIView.as_view()),
    path("books/suggestion/users", BookUserSuggestionListAPIView.as_view()),
]
