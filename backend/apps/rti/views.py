from rest_framework import viewsets
from .models import RTIStep
from .serializers import RTIStepSerializer

class RTIStepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RTIStep.objects.all()
    serializer_class = RTIStepSerializer
