# serializers.py# 
from rest_framework import serializers
import json
from django.forms.models import model_to_dict 
from django.db.models import Model

def serialize_for_hash(instance):
    fields = getattr(instance, "identity_fields", None)
    if not fields:
        raise ValueError(f"{instance.__class__.__name__} must define IDENTITY_FIELDS")

    data = model_to_dict(instance, fields=fields)
    return json.dumps(data, sort_keys=True, separators=(",", ":"))



  
                                                                                                                                                                                                           