import random
from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from api.models.quiz import Quiz, QuizAttempt
from api.models.videos import Rating, Video
from api.serializers.articles import ArticleSerializer
from account.models import Article, ArticleLike,ArticleBookmark, User
from helper.utils.response.response_format import success_response, paginate_success_response, bad_request_response




class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer


    def get_queryset(self, size=None):
        queryset = Article.objects.all()

        if size:
            return queryset.order_by('?')[:int(size)]  
        return queryset 

    def get(self, request, *args, **kwargs):
        size = request.GET.get("page_size")
        return success_response(
            data=self.serializer_class(self.get_queryset(size=size),many=True).data
        )


    

class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'


    def get(self, request, *args, **kwargs):
        return success_response(
            data=self.serializer_class(self.get_object()).data
        )


    

class ArticleCreate(generics.GenericAPIView):

    serializer_class = ArticleSerializer


    def post(self, request, *args, **kwargs):
        """Create a new article with support for written content, PDF uploads, or external links."""
        print(request.data) 
        serializer = self.get_serializer(data=request.data)

        
        # Handle file uploads for top_image and pdf_file if present
        top_image = 'https://upload.wikimedia.org/wikipedia/commons/b/b6/Gutenberg_Bible%2C_Lenox_Copy%2C_New_York_Public_Library%2C_2009._Pic_01.jpg'
        pdf_file = request.FILES.get('pdf_file', None)
        
        if serializer.is_valid():
            # Create but don't save the article instance yet
            article = serializer.save(top_image=top_image, pdf_file=pdf_file)
            
            # Parse and add tags if provided
            if 'tags' in request.data:
                tags_data = request.data.get('tags')
                
                # Handle tags coming as string (comma separated)
                if isinstance(tags_data, str):
                    tag_names = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
                # Handle tags coming as list
                elif isinstance(tags_data, list):
                    tag_names = tags_data
                else:
                    tag_names = []
                    
            #     # Get or create each tag and add to article
            #     for tag_name in tag_names:
            #         tag, created = Tag.objects.get_or_create(name=tag_name)
            #         article.tags.add(tag)
            
            # # Handle channel assignment if provided
            # channel_name = request.data.get('channel', None)
            # if channel_name:
            #     try:
            #         channel = Channel.objects.get(name=channel_name)
            #         article.channel = channel
            #         article.save()
            #     except Channel.DoesNotExist:
            #         # Optionally create the channel if it doesn't exist
            #         pass
            
            return success_response(
                message="Article created successfully",
                data=serializer.data
            )
        
        return bad_request_response(
            message="Failed to create article",
            errors=serializer.errors
        )



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    

        
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(channel__name__icontains=search_query)
            ).distinct()
        
        channel = self.request.query_params.get('channel', None)
        if channel:
            queryset = queryset.filter(channel__slug=channel)
        
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)
            
        return queryset
    
    # def create(self, request, *args, **kwargs):
    #     # Handle the case when tags come as a string instead of a list
    #     if 'tags' in request.data and isinstance(request.data['tags'], str):
    #         request.data['tags_list'] = [tag.strip() for tag in request.data['tags'].split(',') if tag.strip()]
            
    #     return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True,context={'request': request})
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",2))
        )
    
    # def destroy(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     obj.delete()
    #     return success_response(
    #         message="Article deleted successfully"
    #     )


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Check if the user already liked the video
        if ArticleLike.objects.filter(article=article, user=user).exists():
            return bad_request_response(
                message='You have already liked this article.'
            )

        # Create the like
        ArticleLike.objects.create(article=article, user=user)

        return success_response(
            message='Article liked successfully'
        )


    @action(detail=False, methods=['get'], url_path='recommendation')
    def recommendation(self, request):
        articles = Article.objects.all()

        if articles.count() < 3:
            random_articles = articles
        else:
            random_articles = random.sample(list(articles), 5)  

        serializer = self.get_serializer(random_articles, many=True)
        return success_response(serializer.data)
    


    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Check if the user already bookmarked the article
        if ArticleBookmark.objects.filter(article=article, user=user).exists():
            return bad_request_response(
                message='You have already bookmarked this article.'
            )

        # Create the bookmark
        ArticleBookmark.objects.create(article=article, user=user)

        return success_response(
            message='Article bookmarked successfully'
        )

    @action(detail=True, methods=['delete'])
    def unbookmark(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Try to find and delete the bookmark
        try:
            bookmark = ArticleBookmark.objects.get(article=article, user=user)
            bookmark.delete()
            return success_response(
                message='Article bookmark removed successfully'
            )
        except ArticleBookmark.DoesNotExist:
            return bad_request_response(
                message='You have not bookmarked this article.'
            )

    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        user = request.user
        bookmarked_articles = Article.objects.filter(bookmarks__user=user)
        
        serializer = self.get_serializer(bookmarked_articles, many=True, context={'request': request})
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",2000))
        )
    


from django.db import models
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.utils import timezone

class AllOverviewView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        
        # Get current date and date for the start of the month
        now = timezone.now()
        start_of_month = now.replace(day=1)
        
        # Get total number of students (excluding admins)
        total_students = User.objects.filter(is_admin=False).count()

        # Get number of new students this month
        new_students_this_month = User.objects.filter(
            is_admin=False, created_at__gte=start_of_month).count()

        # Get active students (e.g., students who have logged in or have some activity)
        active_students = User.objects.filter(is_admin=False, last_login__gte=start_of_month).count()

        # Get total videos
        total_videos = Video.objects.count()

        # Get total views for videos
        total_video_views = Video.objects.aggregate(total_views=models.Sum('views'))['total_views'] or 0

        # Get average rating of all videos
        # average_video_rating = Video.objects.aggregate(average_rating=models.Avg('rating'))['average_rating'] or 0
        average_video_rating = Rating.objects.aggregate(average_rating=models.Avg('rating'))['average_rating'] or 0

        # Get total articles
        total_articles = Article.objects.count()

        # Get total likes for articles
        total_article_likes = ArticleLike.objects.aggregate(total_likes=models.Count('article'))['total_likes'] or 0

        # Get total bookmarks for articles
        total_article_bookmarks = ArticleBookmark.objects.count()

        # Get total quizzes
        total_quizzes = Quiz.objects.count()

        # Get average score for quizzes
        average_quiz_score = QuizAttempt.objects.aggregate(average_score=models.Avg('score'))['average_score'] or 0

        # Get the highest score achieved in quizzes
        highest_quiz_score = QuizAttempt.objects.aggregate(max_score=models.Max('score'))['max_score'] or 0

        # Prepare the response
        response = {
            'students': {
                'total': total_students,
                'newThisMonth': new_students_this_month,
                'activeUsers': active_students,
            },
            'videos': {
                'total': total_videos,
                'totalViews': total_video_views,
                'averageRating': average_video_rating,
            },
            'articles': {
                'total': total_articles,
                'totalLikes': total_article_likes,
                'totalBookmarks': total_article_bookmarks,
            },
            'quizzes': {
                'total': total_quizzes,
                'averageScore': average_quiz_score,
                'highestScore': highest_quiz_score,
            }
        }

        # Return the success response with the data
        return success_response(data=response)

    




class LastFourMonthsOverviewView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # Get the current date and the date 4 months ago
        today = timezone.now()
        four_months_ago = today - timedelta(days=120)  # Approx 4 months ago (around 30 days per month)

        # Filter students from the last 4 months
        students_data = User.objects.filter(is_admin=False, created_at__gte=four_months_ago)
        # Group by month and count students
        students_per_month = students_data.annotate(month=TruncMonth('created_at')).values('month').annotate(total_students=models.Count('id')).order_by('month')

        # Get total videos per month
        videos_data = Video.objects.filter(created_at__gte=four_months_ago)
        videos_per_month = videos_data.annotate(month=TruncMonth('created_at')).values('month').annotate(total_videos=models.Count('id')).order_by('month')

        # Get total articles per month
        articles_data = Article.objects.filter(created_at__gte=four_months_ago)
        articles_per_month = articles_data.annotate(month=TruncMonth('created_at')).values('month').annotate(total_articles=models.Count('id')).order_by('month')

        # Get total quizzes per month
        quizzes_data = Quiz.objects.filter(created_at__gte=four_months_ago)
        quizzes_per_month = quizzes_data.annotate(month=TruncMonth('created_at')).values('month').annotate(total_quizzes=models.Count('id')).order_by('month')

        # Now format the result in the required format
        result = []
        for i in range(4):
            month_name = (today - timedelta(days=30 * (3 - i))).strftime('%b')
            student_count = next((item['total_students'] for item in students_per_month if item['month'].month == (today - timedelta(days=30 * (3 - i))).month), 0)
            video_count = next((item['total_videos'] for item in videos_per_month if item['month'].month == (today - timedelta(days=30 * (3 - i))).month), 0)
            article_count = next((item['total_articles'] for item in articles_per_month if item['month'].month == (today - timedelta(days=30 * (3 - i))).month), 0)
            quiz_count = next((item['total_quizzes'] for item in quizzes_per_month if item['month'].month == (today - timedelta(days=30 * (3 - i))).month), 0)
            
            result.append({
                'name': month_name,
                'students': student_count,
                'videos': video_count,
                'articles': article_count,
                'quizzes': quiz_count
            })

        return success_response(data=result)

    

