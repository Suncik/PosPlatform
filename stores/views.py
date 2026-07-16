from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Store, SystemSettings
from .serializers import StoreSerializer, SystemSettingsSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class SystemSettingsAPIView(APIView):
  
    def get(self, request):
        settings = SystemSettings.objects.first()
        if not settings:
            # Agar sozlama hali yaratilmagan bo'lsa, bo'sh obyekt qaytaramiz
            return Response({}, status=status.HTTP_200_OK)
        serializer = SystemSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings = SystemSettings.objects.first()
        if settings:
            serializer = SystemSettingsSerializer(settings, data=request.data, partial=True)
        else:
            serializer = SystemSettingsSerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)