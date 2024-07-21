from django.contrib import admin
from apps.reviews.models import Review
# Register your models here.

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "rating"]
    list_filter = ["book", "user", "book__genre"]
