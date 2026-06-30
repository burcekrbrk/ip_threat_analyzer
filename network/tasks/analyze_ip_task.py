from network.models import IPAnalysis
from network.services.threat_service import ThreatService
from network.services.cache_service import CacheService


# Şimdilik düz bir fonksiyon, Celery'ye bağlarken sadece @shared_task dekoratörü ekleyeceğiz
def analyze_subnet_ips_task(subnet_id: int):
    """
    Bir subnet'e ait tüm PENDING durumundaki IP'leri arka planda analiz eder.
    """
    ips_to_analyze = IPAnalysis.objects.filter(subnet_id=subnet_id, status='PENDING')

    for ip_obj in ips_to_analyze:
        # 1. Önce Cache kontrolü (Mükerrer işlemi engelleme)
        cached_status = CacheService.get_ip_status(ip_obj.ip_address)

        if cached_status:
            ip_obj.status = cached_status
        else:
            # 2. Cache'de yoksa analiz et (0.5 sn sürecek)
            result_status = ThreatService.analyze_ip(ip_obj.ip_address)
            ip_obj.status = result_status
            # 3. Cache'e yaz
            CacheService.set_ip_status(ip_obj.ip_address, result_status)

        ip_obj.save()