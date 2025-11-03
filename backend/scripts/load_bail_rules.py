# script to load bail rules
import os
import django
import sys

# --- Add these lines to fix the path ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
# --- End of fix ---

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.bail.models import BailRule

def run():
    if BailRule.objects.exists():
        print("Bail rule data already loaded. Exiting.")
        return

    print("Loading sample bail rules...")
    
    BailRule.objects.bulk_create([
        BailRule(section_no="302", offence_type="Murder", description="Punishment for murder.", bailable=False),
        BailRule(section_no="307", offence_type="Attempt to murder", description="Attempt to commit murder.", bailable=False),
        BailRule(section_no="323", offence_type="Punishment for voluntarily causing hurt", description="Simple hurt.", bailable=True),
        BailRule(section_no="504", offence_type="Intentional insult with intent to provoke breach of the peace", description="Insult to provoke.", bailable=True),
        BailRule(section_no="420", offence_type="Cheating and dishonestly inducing delivery of property", description="Cheating.", bailable=False)
    ])
    
    print("Successfully loaded sample bail rules.")

if __name__ == "__main__":
    run()