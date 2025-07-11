from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    price = models.FloatField(default=0.0)

    authors = models.ManyToManyField(Author, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    isbn_10 = models.CharField(max_length=10, blank=True, unique=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, unique=True, null=True)

    language = models.CharField(max_length=50, default='English')
    publication_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)

    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
        ]

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{str(uuid.uuid4())[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title