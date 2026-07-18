from django.core.management.base import BaseCommand

from account.models import Article
from api.models.other import Category, Tag

# Branch
class Command(BaseCommand):
    help = 'Migrate data from the old database to the new database'

    def handle(self, *args, **kwargs):

        # Use the old database connection
        tags_list = [
            "React",
            "Tailwind CSS",
            "Web Development",
            "Frontend",
            "React Hooks",
            "JavaScript",
            "CSS",
            "Grid",
            "Web Design",
            "Responsive Design",
            "Node.js",
            "Express",
            "MongoDB",
            "Full Stack",
            "TypeScript",
            "UI Design"
        ]
        category_list = [
            "Web Development",
            "Programming",
            "Databases",
            "Data Science",
            "UI Design"
        ]
        for t in tags_list:
            obj, _ = Tag.objects.get_or_create(name=t)
            obj.save()

        for t in category_list:
            obj, _ = Category.objects.get_or_create(name=t)
            obj.save()

        self.stdout.write(self.style.SUCCESS('Data migration completed successfully.'))
