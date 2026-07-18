# models.py
from django.db import models
from django.utils.text import slugify
import uuid
import os

from account.models import User
from api.models.other import Category, Tag

def video_upload_path(instance, filename):
    # Generate a unique filename with original extension
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('videos', filename)

def thumbnail_upload_path(instance, filename):
    # Generate a unique filename with original extension
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('thumbnails', filename)




class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    tags = models.ManyToManyField(Tag, blank=True, related_name='videos')
    video_file = models.FileField(upload_to=video_upload_path)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

    def get_average_rating(self):
        # Calculate the average rating of the video
        ratings = self.ratings.all()
        if ratings:
            return sum([rating.rating for rating in ratings]) / len(ratings)
        return None  # No ratings yet

    def get_likes_count(self):
        # Return the number of likes for the video
        return self.likes.count()
    




class Rating(models.Model):
    video = models.ForeignKey(Video, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) 
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('video', 'user')  

    def __str__(self):
        return f"{self.user.username} rated {self.video.title} {self.rating}"



class Like(models.Model):
    video = models.ForeignKey(Video, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video', 'user') 

    def __str__(self):
        return f"{self.user.email} liked {self.video.title}"
