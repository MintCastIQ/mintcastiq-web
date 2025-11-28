# views.py
from rest_framework import viewsets
from .models import DimCard
from .serializers import DimCardSerializer

class DimCardViewSet(viewsets.ModelViewSet):
    queryset = DimCard.objects.all()
    serializer_class = DimCardSerializer
