from rest_framework.serializers import ModelSerializer, DecimalField

from apps.books.models import Book
from apps.reviews.api.serializers import ReviewSerializer


class BookSerializer(ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["title", "author", "genre", "review_set"]


class BookSuggestionSerializer(ModelSerializer):
    possible_rate = DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "genre",
            "possible_rate",
        ]
