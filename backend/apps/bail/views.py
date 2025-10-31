from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BailRule
from .serializers import BailRuleSerializer
from .services import get_bail_information

class BailRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BailRule.objects.all()
    serializer_class = BailRuleSerializer

    @action(detail=False, methods=["post"])
    def check(self, request):
        section = request.data.get("section_no")
        offence = request.data.get("offence")
        result = get_bail_information(section, offence)
        return Response(result)
