from rest_framework import serializers
from .models import RTIStep

class RTIStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RTIStep
        fields = "__all__"
