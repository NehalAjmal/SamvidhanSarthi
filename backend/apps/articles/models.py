from django.db import models

class Article(models.Model):
    part = models.CharField(max_length=50, blank=True)
    chapter = models.CharField(max_length=100, blank=True)
    article_no = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    simple_text_en = models.TextField()
    simple_text_hi = models.TextField(blank=True, null=True)
    original_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["article_no"]

    def __str__(self):
        return f"Article {self.article_no}: {self.title}"
