from rest_framework import serializers
from network.models import Subnet

class SubnetInputSerializer(serializers.Serializer):
    # Kullanıcıdan sadece tek bir string alacağız (Örn: "10.0.0.0/24")
    subnet = serializers.CharField(max_length=255)

class SubnetDetailSerializer(serializers.ModelSerializer):
    # Bu subnet'e ait IP'leri de içinde listeleyebilmek için yukarıdaki serializer'ı bağlıyoruz
    ip_addresses = serializers.SerializerMethodField()

    class Meta:
        model = Subnet
        fields = ['id', 'network_address', 'cidr', 'ip_version', 'created_at', 'ip_addresses']

    def get_ip_addresses(self, obj):
        # Sayfalama (Pagination) mantığını View içinde kuracağımız için şimdilik ilk 10 tanesini gösterelim
        # (Tam sayfalama kurallarını bir sonraki adımda `pagination.py` ile yapacağız)
        ips = obj.ip_addresses.all()[:10]
        from network.serializers.analysis_serializer import IPAnalysisSerializer
        return IPAnalysisSerializer(ips, many=True).data