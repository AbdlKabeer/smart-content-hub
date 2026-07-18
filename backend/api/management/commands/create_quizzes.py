import random
from django.core.management.base import BaseCommand
from faker import Faker

from api.models.other import Category, Tag
from api.models.quiz import Option, Question, Quiz


class Command(BaseCommand):
    help = 'Create 2 quizzes with 5 questions and random tags for each category'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for h in Quiz.objects.all():
            h.delete()
        # Get all categories in the system
        categories = Category.objects.all()

        # Ensure we have at least one user to assign as created_by
        user = None

        # Check if there are categories
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found in the system!'))
            return

        for category in categories:
            for _ in range(2):  # Create 2 quizzes per category
                quiz = Quiz.objects.create(
                    title=fake.sentence(nb_words=3),
                    description=fake.paragraph(nb_sentences=2),
                    category=category,
                    level=random.choice(['Easy', 'Medium', 'Hard']),
                    estimated_time=random.randint(10, 30),
                    created_by=user,  # Assign to the first user, can be random if needed
                )

                # Add random tags to the quiz (max 3 random tags)
                tags = Tag.objects.all()
                random_tags = random.sample(list(tags), min(3, tags.count()))
                quiz.tags.set(random_tags)

                # Create 5 random questions for the quiz
                for i in range(5):
                    question = Question.objects.create(
                        quiz=quiz,
                        text=fake.sentence(nb_words=6),
                        explanation=fake.text(),
                    )

                    # Create 4 random options for each question
                    correct_option = random.randint(1, 4)
                    for option_num in range(1, 5):
                        Option.objects.create(
                            question=question,
                            text=fake.word(),
                            is_correct=(option_num == correct_option),
                            option_id=str(option_num),
                        )

                self.stdout.write(self.style.SUCCESS(f'Successfully created 2 quizzes with 5 questions for category: {category.name}'))
