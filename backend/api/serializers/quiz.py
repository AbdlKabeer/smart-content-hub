# # serializers.py
# from rest_framework import serializers

# from api.models.other import Tag
# from api.models.quiz import Quiz, Option, Question
# from api.serializers.videos import CategorySerializer, TagSerializer


# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = ['id', 'option_id', 'text', 'is_correct']

# class QuestionSerializer(serializers.ModelSerializer):
#     options = OptionSerializer(many=True)
    
#     class Meta:
#         model = Question
#         fields = ['id', 'text', 'options', 'explanation']


# class QuizSerializer(serializers.ModelSerializer):
#     questions = QuestionSerializer(many=True)
#     category = CategorySerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=True)
#     tags_ids = serializers.CharField(write_only=True)

#     class Meta:
#         model = Quiz
#         fields = ['id', 'title', 'description',"tags_ids", 'category', 'level', 
#                  'estimated_time', 'created_at', 'questions', 'tags',]
#         read_only_fields = ['created_at']
    
#     def create(self, validated_data):
#         questions_data = validated_data.pop('questions')
#         tags_list = validated_data.pop('tags_ids', '')
        
#         # Create the quiz
#         quiz = Quiz.objects.create(**validated_data)
        
#         # Add tags
#         # Add tags by ID
#         for tag_id in tags_list.split(","):
#             try:
#                 tag = Tag.objects.get(id=tag_id)
#                 quiz.tags.add(tag)
#             except Tag.DoesNotExist:
#                 continue  # Skip invalid tag IDs
        
#         # Add questions
#         for question_data in questions_data:
#             options_data = question_data.pop('options')
#             question = Question.objects.create(quiz=quiz, **question_data)
            
#             # Add options to the question
#             for option_data in options_data:
#                 Option.objects.create(question=question, **option_data)
        
#         return quiz
    
#     def to_internal_value(self, data):
#         # Transform frontend data format to match serializer expectations
#         if 'questions' in data:
#             for question in data['questions']:
#                 # Handle the correctOptionId by marking the correct option
#                 correct_id = question.pop('correctOptionId', None)
#                 if correct_id and 'options' in question:
#                     for option in question['options']:
#                         option['is_correct'] = option['id'] == correct_id
        
#         # Handle tags
#         if 'tags' in data:
#             data['tags_list'] = data.pop('tags')
        
#         return super().to_internal_value(data)




from rest_framework import serializers

from api.models.other import Category, Tag
from api.models.quiz import Quiz, Option, Question
from api.serializers.videos import CategorySerializer, TagSerializer


class OptionSerializer(serializers.ModelSerializer):
    option_id = serializers.CharField(required=True)
    
    class Meta:
        model = Option
        fields = ['id', 'option_id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'explanation']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    estimated_time = serializers.IntegerField(required=True)
    category_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'tags_ids', 'category',"category_id", 'level', 
                 'estimated_time', 'created_at', 'questions', 'tags']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        category_id = validated_data.pop('category_id')
        tags_ids = validated_data.pop('tags_ids', [])
        
        
        category = Category.objects.get(id=category_id)
        validated_data['category']= category
        # Create the quiz
        quiz = Quiz.objects.create(**validated_data)
        
        # Add tags
        for tag_id in tags_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
                quiz.tags.add(tag)
            except Tag.DoesNotExist:
                continue  # Skip invalid tag IDs
        
        # Add questions
        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(quiz=quiz, **question_data)
            
            # Add options to the question
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)
        
        return quiz
    
    def to_internal_value(self, data):
        # Handle category ID mapping
        if 'category' in data and isinstance(data['category'], str):
            # Assuming category ID is passed as a string
            from api.models.videos import Category
            try:
                Category.objects.get(id=data['category'])
            except Category.DoesNotExist:
                raise serializers.ValidationError({'category': ['Invalid category ID']})
        
        # Handle level/difficulty mapping
        if 'difficulty' in data:
            data['level'] = data.pop('difficulty')
        
        # Handle estimatedTime -> estimated_time
        if 'estimatedTime' in data:
            data['estimated_time'] = data.pop('estimatedTime')
        
        # Handle tags -> tags_ids
        if 'tags' in data:
            data['tags_ids'] = data.pop('tags')
        
        # Transform questions for serializer
        if 'questions' in data:
            for question in data['questions']:
                # Map correctOptionId to is_correct on options
                correct_id = question.pop('correctOptionId', None)
                
                if 'options' in question:
                    for option in question['options']:
                        # Set option_id from id
                        option['option_id'] = option['id']
                        # Set is_correct based on correctOptionId
                        option['is_correct'] = option['id'] == correct_id
        
        return super().to_internal_value(data)