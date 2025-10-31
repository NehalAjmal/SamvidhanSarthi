from django.db import models

class RTIStep(models.Model):
    step_no = models.IntegerField()
    heading = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        ordering = ["step_no"]

    def __str__(self):
        return f"Step {self.step_no}: {self.heading}"
