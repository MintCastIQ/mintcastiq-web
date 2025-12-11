# views.py
from rest_framework import viewsets
from mintcastiq.models import DimCard
from mintcastiq.serializers import serialize_for_hash

class DimCardViewSet(viewsets.ModelViewSet):
    queryset = DimCard.objects.all()
    
