from django.urls import path

from apps.reviews.api.views import (
    CreateReviewAPIView,
    UpdateReviewAPIView,
    DestroyReviewAPIView,
)

urlpatterns = [
    path("reviews/add", CreateReviewAPIView.as_view()),
    path("reviews/update", UpdateReviewAPIView.as_view()),
    path("reviews/<int:book_id>/delete", DestroyReviewAPIView.as_view()),
]
