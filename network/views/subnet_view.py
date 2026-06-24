from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from network.serializers.subnet_serializer import SubnetInputSerializer, SubnetDetailSerializer
from network.services.subnet_service import SubnetService


class SubnetAnalysisView(APIView):
    """
    POST: Yeni bir subnet analiz isteği alır, IP'leri türetir.
    """

    def post(self, request):
        serializer = SubnetInputSerializer(data=request.data)
        if serializer.is_valid():
            subnet_str = serializer.validated_data['subnet']

            # Servis katmanımızı çağırıp subnet ve IP'leri oluşturuyoruz
            subnet, created = SubnetService.get_or_create_subnet_and_ips(subnet_str)

            # Sonucu kullanıcıya dönüyoruz
            response_serializer = SubnetDetailSerializer(subnet)

            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(response_serializer.data, status=status_code)

        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)