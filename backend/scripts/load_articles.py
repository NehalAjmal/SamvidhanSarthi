# script to load article data
import os
import django
import csv

# Set up the Django environment
# This points Django to your project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Now you can import your models
from apps.articles.models import Article

# Define the path to your CSV file
CSV_PATH = 'backend/dataset/articles.csv'

def run():
    if Article.objects.exists():
        print("Article data already loaded. Exiting.")
        return

    print("Loading Constitution articles...")

    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        articles_to_create = []
        for row in reader:
            # Map CSV columns to model fields
            article = Article(
                part=row.get('part', 'NONE'),
                chapter=row.get('chapter', 'NONE'),
                article_no=row.get('article_no', ''),
                title=row.get('title', ''),
                simple_text_en=row.get('simple_text_en', ''),
                simple_text_hi=row.get('simple_text_hi', ''),
                original_text=row.get('original_text', '')
            )
            articles_to_create.append(article)
        
        # Use bulk_create for efficiency
        Article.objects.bulk_create(articles_to_create)

    print(f"Successfully loaded {len(articles_to_create)} articles into the database.")

if __name__ == "__main__":
    run()