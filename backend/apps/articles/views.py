from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Article
from django.db import models
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides /api/articles/ and /api/articles/search/?q=... endpoints
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["article_no", "title", "simple_text_en", "simple_text_hi", "original_text"]

    @action(detail=False, methods=["get"], url_path="search")
    def search_articles(self, request):
        query = request.query_params.get("q", "")
        language = request.query_params.get("lang", "en")

        # 1. FIXED QUERY: Search title AND original_text
        qs = Article.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(original_text__icontains=query)
        )

        data = []
        for art in qs[:30]:
            # 2. FIXED RESPONSE: Return 'original_text' as content
            # (since simple_text_en is empty in your CSV)
            content_to_return = art.simple_text_hi if language == "hi" else art.original_text
            
            # Use original_text if HI is also blank
            if language == "hi" and not art.simple_text_hi:
                content_to_return = art.original_text

            data.append({
                "article_no": art.article_no,
                "title": art.title,
                "content": content_to_return 
            })
        return Response(data)