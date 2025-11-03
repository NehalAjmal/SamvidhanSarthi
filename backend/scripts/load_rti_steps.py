# script to load RTI steps
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

from apps.rti.models import RTIStep

def run():
    if RTIStep.objects.exists():
        print("RTI step data already loaded. Exiting.")
        return

    print("Loading sample RTI steps...")
    
    RTIStep.objects.bulk_create([
        RTIStep(step_no=1, heading="Identify the Department", details="Find the correct Public Information Officer (PIO) for the department you need information from."),
        RTIStep(step_no=2, heading="Draft Your Application", details="Write your questions clearly. You do not need to give a reason for asking. Pay the ₹10 fee."),
        RTIStep(step_no=3, heading="Submit the Application", details="Submit your application to the PIO online or offline. Keep a copy for your records."),
        RTIStep(step_no=4, heading="Wait for Response (30 Days)", details="The PIO must reply within 30 days. If it concerns life or liberty, the limit is 48 hours."),
        RTIStep(step_no=5, heading="First Appeal", details="If you get no response or are unsatisfied, you can file a First Appeal with the First Appellate Authority (FAA) within 30 days."),
        RTIStep(step_no=6, heading="Second Appeal", details="If still unsatisfied, you can file a Second Appeal with the Central/State Information Commission within 90 days.")
    ])
    
    print("Successfully loaded sample RTI steps.")

if __name__ == "__main__":
    run()