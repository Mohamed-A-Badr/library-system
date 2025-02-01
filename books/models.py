from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from authors.models import Author


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    page_count = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Book must have at least one page."),
            MaxValueValidator(10000, message="Book must have at most 10,000 page."),
        ],
        blank=True,
        null=True,
    )
    categories = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["isbn", "title"])]

    def __str__(self):
        return self.title
