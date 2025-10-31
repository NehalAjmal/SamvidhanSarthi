from django.db import models

class BailRule(models.Model):
    section_no = models.CharField(max_length=50)
    offence_type = models.CharField(max_length=255)
    description = models.TextField()
    bailable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.section_no} - {self.offence_type}"
