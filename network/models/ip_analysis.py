from django.db import models
from .subnet import Subnet

class IPAnalysis(models.Model):
    STATUS_CHOICES = [
        ('SAFE', 'Safe'),
        ('MALICIOUS', 'Malicious'),
        ('PENDING', 'Pending'), # Celery arka planda işlerken ilk durum pending olabilir
    ]

    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE, related_name='ip_addresses')
    ip_address = models.GenericIPAddressField() # Hem IPv4 hem IPv6 destekler
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "IP Analyses"
        unique_together = ('subnet', 'ip_address')

    def __str__(self):
        return f"{self.ip_address} - {self.status}"