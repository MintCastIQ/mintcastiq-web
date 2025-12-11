# serializers.py# 
from rest_framework import serializers
import json
from django.forms.models import model_to_dict 

def serialize_for_hash(instance) -> str:
    """
    Convert a Django model instance into a stable JSON string
    suitable for hashing.
    """
    data = model_to_dict(instance)

    # Sort keys to ensure deterministic output
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


  
                                                                                                                                                                                                           