from rest_framework.generics import ListAPIView
from network.models import IPAnalysis
from network.serializers.analysis_serializer import IPAnalysisSerializer
from network.pagination import StandardResultsSetPagination

class IPAnalysisListView(ListAPIView):
    """
    GET: Sistemdeki tüm analiz sonuçlarını sayfalanmış olarak listeler.
    Sorgu parametresi olarak subnet id veya ip filtresi alabilir.
    """
    serializer_class = IPAnalysisSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = IPAnalysis.objects.all().order_by('-checked_at')
        subnet_id = self.request.query_params.get('subnet_id')
        if subnet_id:
            queryset = queryset.filter(subnet_id=subnet_id)
        return queryset