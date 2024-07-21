from django.urls import path

from apps.books.api.views import BookListAPIView,BookGenreSuggestionListAPIView

urlpatterns = [
    path("books", BookListAPIView.as_view()),
    path("books/suggestion/genre", BookGenreSuggestionListAPIView.as_view()),
]
