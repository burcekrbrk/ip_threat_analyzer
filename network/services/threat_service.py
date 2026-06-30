import random
import time
from network.models import IPAnalysis


class ThreatService:
    @staticmethod
    def analyze_ip(ip_address: str) -> str:
        """
        IP adresinin tehdit durumunu simüle eder.
        Sanki dış bir API'ye istek atıyormuş gibi 0.5 saniye gecikme ekleyelim
        ki asenkron (Celery) ihtiyacını canlı canlı hissedelim.
        """
        time.sleep(0.5)

        # Basit bir algoritmik mantık: IP'nin son karakterine bakalım
        # Veya tamamen rastgele: return random.choice(['SAFE', 'MALICIOUS'])
        try:
            last_digit = int(ip_address.split('.')[-1])
            return 'SAFE' if last_digit % 2 != 0 else 'MALICIOUS'
        except (ValueError, IndexError):
            # IPv6 veya ayrıştırma hatası durumunda rastgele dönelim
            return random.choice(['SAFE', 'MALICIOUS'])