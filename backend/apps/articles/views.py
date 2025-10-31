from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Article
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

        qs = Article.objects.filter(
            simple_text_en__icontains=query
        ) | Article.objects.filter(title__icontains=query)

        data = []
        for art in qs[:30]:
            data.append({
                "article_no": art.article_no,
                "title": art.title,
                "content": art.simple_text_hi if language == "hi" else art.simple_text_en
            })
        return Response(data)
