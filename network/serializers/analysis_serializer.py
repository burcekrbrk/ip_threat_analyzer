from rest_framework import serializers
from network.models import IPAnalysis

class IPAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAnalysis
        fields = ['id', 'ip_address', 'status', 'checked_at']