import ipaddress
from rest_framework.exceptions import ValidationError
from network.models import Subnet, IPAnalysis


class SubnetService:

    @staticmethod
    def validate_and_parse(ip_with_mask: str):
        """
        Girdi formatını doğrular ve IP versiyonu ile maske sınırlarını kontrol eder.
        """
        try:
            # ipaddress kütüphanesi hem IPv4 hem IPv6 format kontrolünü otomatik yapar
            network = ipaddress.ip_network(ip_with_mask, strict=False)
        except ValueError:
            raise ValidationError({"error": "Geçersiz IPv4 veya IPv6 formatı."})[cite: 13]

        # Sınır Kontrolleri (Validation) [cite: 11]
        if network.version == 4 and network.prefixlen > 24:
            raise ValidationError({"error": "IPv4 için maksimum subnet mask değeri 24 olmalıdır."})[cite: 14]
        if network.version == 6 and network.prefixlen > 64:
            raise ValidationError({"error": "IPv6 için maksimum subnet mask değeri 64 olmalıdır."})[cite: 15]

        return network

    @classmethod
    def get_or_create_subnet_and_ips(cls, ip_with_mask: str):
        """
        Subnet'i ve altındaki tüm geçerli IP'leri veritabanına kaydeder (veya var olanı döner).
        """
        network = cls.validate_and_parse(ip_with_mask)

        # Mükerrer istekleri engellemek için önce veritabanına bakıyoruz
        subnet, created = Subnet.objects.get_or_create(
            network_address=str(network.network_address),
            cidr=network.prefixlen,
            defaults={'ip_version': network.version}
        )

        # Eğer yeni oluşturulduysa alt ağdaki IP'leri çıkarıp PENDING olarak kaydedelim
        if created:
            ip_objects = []
            # hosts() metodu ağ ve yayın (broadcast) adresleri dışındaki geçerli IP'leri döner
            for ip in network.hosts():
                ip_objects.append(
                    IPAnalysis(subnet=subnet, ip_address=str(ip), status='PENDING')
                )

            # Performans için toplu ekleme (Bulk create) yapıyoruz
            if ip_objects:
                IPAnalysis.objects.bulk_create(ip_objects)
            # ---- YENİ EKLENEN KISIM ----
            # Normalde bunu Celery (.delay()) tetikleyecek, şimdilik senkron çağırıyoruz
            from network.tasks.analyze_ip_task import analyze_subnet_ips_task
            analyze_subnet_ips_task(subnet.id)
            # ----------------------------
        return subnet, created