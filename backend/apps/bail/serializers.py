from rest_framework import serializers
from .models import BailRule

class BailRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BailRule
        fields = "__all__"
