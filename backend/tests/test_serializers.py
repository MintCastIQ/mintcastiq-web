from django.test import TestCase
from mintcastiq.models import DimSet
from domain.serializers import serialize_for_hash


class TestHashingSerializer(TestCase):

    def setUp(self):
        self.dim = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2024",
            subset_name="Base",
        )

    def test_serializer_outputs_json(self):
        pass

    def test_serializer_includes_identity_fields(self):
        pass

    def test_serializer_excludes_non_identity_fields(self):
        pass

    def test_serializer_is_deterministic(self):
        pass

    def test_serializer_raises_on_missing_identity_fields(self):
        pass
