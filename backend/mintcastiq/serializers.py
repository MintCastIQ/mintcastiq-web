# serializers.py# 
from rest_framework import serializers
from .models import DimCard

class DimCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCard
        fields = "__all__"

  
                                                                                                                                                                                                           