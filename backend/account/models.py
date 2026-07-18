import random, uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create a regular user with the given email and password.
        """
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Optional
    current_year_level = models.IntegerField(
        choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')],
        null=True,
        blank=True
    )
    previous_year_performance = models.CharField(
        max_length=20,
        choices=[('First Class', 'First Class'), ('2:1', '2:1'), ('2:2', '2:2'), ('Third Class', 'Third Class')],
        null=True,
        blank=True
    )
    preferred_content = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ('Video', 'Video'),
            ('Article', 'Article'),
            ('Quiz', 'Quiz'),
        ]
    )
    study_preference = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ('Morning', 'Morning'),
            ('Night', 'Night'),
        ]
    )
    current_year_level = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year'),

        ]
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email




# class Article(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)
#     authors = models.TextField(blank=True)  # Store authors as a text field, comma-separated
#     publish_date = models.TextField(null=True, blank=True)
#     source_url = models.URLField(max_length=2000)
#     text = models.TextField()
#     keywords = models.TextField(blank=True)  # Store keywords as a comma-separated string
#     top_image = models.URLField(max_length=2000, blank=True, null=True)
#     meta_description = models.TextField(blank=True)
#     summary = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)

#     def __str__(self):
#         return self.title


#     def get_likes_count(self):
#         return self.articles.count()


class Article(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('written', 'Written Content'),
        ('pdf', 'PDF Document'),
        ('external', 'External Link'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    authors = models.TextField(blank=True)
    publish_date = models.TextField(null=True, blank=True)
    source_url = models.URLField(max_length=2000, blank=True, null=True)
    text = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    top_image = models.URLField(max_length=2000, blank=True, null=True)
    meta_description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # New fields for content type handling
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='written')
    pdf_file = models.FileField(upload_to='articles/pdfs/', blank=True, null=True)
    external_link = models.URLField(max_length=2000, blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.articles.count()


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, related_name='articles', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user') 

    def __str__(self):
        return f"{self.user.email} liked {self.video.title}"


class ArticleBookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.email} bookmarked {self.article.title}"

    