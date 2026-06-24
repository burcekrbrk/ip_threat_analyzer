from django.db import models

class Subnet(models.Model):
    # Ağ adresi ve maske bilgisini tutar (Örn: "10.0.0.0/24" veya "2001:db8::/64")
    network_address = models.CharField(max_length=255, unique=True)
    cidr = models.IntegerField() # Subnet mask değeri (24, 64 vb.)
    ip_version = models.IntegerField(choices=((4, 'IPv4'), (6, 'IPv6')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.network_address}/{self.cidr}"