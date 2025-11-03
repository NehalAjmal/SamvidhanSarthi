import os
import django
import csv
import sys  # <-- Add this

# --- Add these lines to fix the path ---
# Get the directory of the script (backend/scripts)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (backend/) and add it to sys.path
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
# --- End of fix ---

# Set up the Django environment
# This will now correctly find 'backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Now you can import your models
from apps.articles.models import Article

# Define the path to your CSV file
CSV_PATH = 'backend/dataset/articles.csv'  # This path is relative to the 'backend' folder now

def run():
    if Article.objects.exists():
        print("Article data already loaded. Exiting.")
        return

    print("Loading Constitution articles...")
    
    # --- Fix CSV Path ---
    # Build a full path to the CSV from the project root
    full_csv_path = os.path.join(project_root, 'dataset/articles.csv')
    
    with open(full_csv_path, mode='r', encoding='utf-8') as f: # <-- Use full_csv_path
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