from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BailRule
from .serializers import BailRuleSerializer

class BailRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BailRule.objects.all()
    serializer_class = BailRuleSerializer

    @action(detail=False, methods=["post"])
    def check(self, request):
        section = request.data.get("section_no", "").strip()
        rule = BailRule.objects.filter(section_no__iexact=section).first()
        if rule:
            return Response({
                "found": True,
                "bailable": rule.bailable,
                "description": rule.description,
            })
        return Response({"found": False, "message": "Section not found"})
