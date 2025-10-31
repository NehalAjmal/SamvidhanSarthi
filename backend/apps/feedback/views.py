from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by("-created_at")
    serializer_class = FeedbackSerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        avg = self.queryset.aggregate_avg = self.queryset.aggregate_avg = self.queryset.aggregate()
        count = self.queryset.count()
        return Response({"total_feedbacks": count})
