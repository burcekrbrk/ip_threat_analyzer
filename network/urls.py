from django.urls import path
from network.views.subnet_view import SubnetAnalysisView
from network.views.analysis_view import IPAnalysisListView

urlpatterns = [
    path('analyze/', SubnetAnalysisView.as_view(), name='subnet-analyze'),
    path('results/', IPAnalysisListView.as_view(), name='analysis-results'), # Yeni eklenen
]