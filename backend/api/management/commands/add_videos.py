import random
import uuid
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
import os

from api.models.other import Category, Tag
from api.models.videos import Video

class Command(BaseCommand):
    help = 'Creates 20 new videos with existing categories and tags.'

    def handle(self, *args, **kwargs):
        # Fetch all categories and tags from the database
        categories = Category.objects.all()
        tags = Tag.objects.all()

        if not categories:
            self.stdout.write(self.style.ERROR("No categories found!"))
            return

        if not tags:
            self.stdout.write(self.style.ERROR("No tags found!"))
            return

        # Generate 20 video entries
        for _ in range(20):
            title = f"Sample Video Title {uuid.uuid4().hex[:8]}"
            description = f"This is a sample description for the video {title}."
            category = random.choice(categories)
            selected_tags = random.sample(list(tags), random.randint(1, 5))  # Select 1 to 5 random tags

            # Generate video file path (for this example, you would replace it with actual file paths)
            video_file_path = 'sample-video.mp4'  # Replace with your file path
            thumbnail_path = 'thumbnail.jpg'  # Replace with your file path
            
            # Create video file and thumbnail as File objects (mocking for demonstration purposes)
            video_file = File(open(video_file_path, 'rb'))
            thumbnail = File(open(thumbnail_path, 'rb'))
            
            # Create video object and save
            video = Video(
                title=title,
                description=description,
                category=category,
                video_file=video_file,
                thumbnail=thumbnail,
            )
            video.save()  # Save video to get ID for slug generation
            
            # Assign random tags to the video
            video.tags.set(selected_tags)
            
            # Print success message
            self.stdout.write(self.style.SUCCESS(f"Video '{video.title}' created successfully!"))
            
            # Close file objects after saving
            video_file.close()
            thumbnail.close()
