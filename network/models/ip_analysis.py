from django.db import models


class IPAnalysis(models.Model):

    STATUS_CHOICES = (
        ("safe", "Safe"),
        ("malicious", "Malicious"),
    )

    ip_address = models.GenericIPAddressField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    subnet = models.ForeignKey(
        "Subnet",
        on_delete=models.CASCADE,
        related_name="analyses"
    )

    analyzed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.ip_address} - {self.status}"