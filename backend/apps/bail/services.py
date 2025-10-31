# business logic for bail
from .models import BailRule

def get_bail_information(section_no: str = None, offence: str = None):
    """
    Core logic for bail reckoner — looks up bailability and gives reasoning.
    """
    if section_no:
        rule = BailRule.objects.filter(section_no__iexact=section_no).first()
    elif offence:
        rule = BailRule.objects.filter(offence_type__icontains=offence).first()
    else:
        return {"found": False, "message": "Please provide a section or offence."}

    if not rule:
        return {"found": False, "message": "No matching rule found."}

    return {
        "found": True,
        "section_no": rule.section_no,
        "offence": rule.offence_type,
        "bailable": rule.bailable,
        "description": rule.description
    }
