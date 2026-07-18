from rest_framework import serializers

from account.models import Article, ArticleBookmark, ArticleLike




class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_bookmarked = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = [
            'id','title','authors',"publish_date",
            'source_url','text','keywords','top_image',
            "meta_description","summary",'created_at','likes_count',
            "has_liked",'content_type','external_link','pdf_file',
            'bookmarks_count', 'has_bookmarked'
        ]

    def get_likes_count(self, obj:Article):
        return obj.get_likes_count()

    def get_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return ArticleLike.objects.filter(article=obj, user=request.user).exists()
        return False
    
    def get_bookmarks_count(self, obj:Article):
        return obj.bookmarks.count()

    def get_has_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return ArticleBookmark.objects.filter(article=obj, user=request.user).exists()
        return False