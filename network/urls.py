from django.urls import path
from network.views.subnet_view import SubnetAnalysisView

urlpatterns = [
    path('analyze/', SubnetAnalysisView.as_view(), name='subnet-analyze'),
]