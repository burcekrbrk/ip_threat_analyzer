from django.core.cache import cache

class CacheService:
    CACHE_TIMEOUT = 24 * 60 * 60  # 24 saat (saniye cinsinden)

    @classmethod
    def get_ip_status(cls, ip_address: str):
        """Cache'den IP durumunu sorgular."""
        return cache.get(f"ip_status:{ip_address}")

    @classmethod
    def set_ip_status(cls, ip_address: str, status: str):
        """IP durumunu 24 saatliğine cache'e yazar."""
        cache.set(f"ip_status:{ip_address}", status, timeout=cls.CACHE_TIMEOUT)