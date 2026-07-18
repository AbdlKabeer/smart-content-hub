# models.py
import uuid
from django.db import models
from account.models import User
from api.models.other import Category, Tag


class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes")
    tags = models.ManyToManyField(Tag,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL , null=True, blank=True, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    option_id = models.CharField(max_length=10) 
    
    def __str__(self):
        return f"{self.option_id}: {self.text}"



class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')

    score = models.FloatField()

    attempted_at = models.DateTimeField(auto_now_add=True)

    comments = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=[('Completed', 'Completed'), ('Abandoned', 'Abandoned')],
        default='Completed'
    )


    def __str__(self):
        return f"Attempt by {self.user} on {self.quiz.title} with score {self.score}%"

