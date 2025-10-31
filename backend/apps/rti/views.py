from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RTIStep
from .serializers import RTIStepSerializer
from .services import generate_rti_template

class RTIStepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RTIStep.objects.all()
    serializer_class = RTIStepSerializer

    @action(detail=False, methods=["post"], url_path="generate")
    def generate_rti(self, request):
        data = request.data
        name = data.get("name", "")
        address = data.get("address", "")
        info = data.get("info_sought", "")
        public_authority = data.get("public_authority", "")
        text = generate_rti_template(name, address, info, public_authority)
        return Response({"template": text})
