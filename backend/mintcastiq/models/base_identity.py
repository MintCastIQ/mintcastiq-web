from django.db import models
from domain.hashing import hash_string


class BaseIdentity(models.Model):
    """
    Shared identity + lifecycle foundation for all canonical dimension tables.

    Responsibilities:
    - Deterministic identity_string based on model-defined fields
    - Stable checksum hashing (identity only)
    - Friendly name generation
    - Enforce identity immutability after creation
    - Provide canonicalize() hook for normalization
    - Provide create() helper for contributor-safe instantiation
    """

    # Subclasses MUST override this with a tuple
    identity_fields = ()
    friendly_name_template = None  # e.g. "{set_year} {publisher} {set_name}"

    # Lifecycle
    status = models.CharField(max_length=32, default="ACTIVE")

    # Identity + hashing
    checksum = models.CharField(max_length=64, editable=False)

    class Meta:
        abstract = True

    # ------------------------------------------------------------
    # Class validation (runtime safety)
    # ------------------------------------------------------------
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not isinstance(cls.identity_fields, tuple):
            raise TypeError(
                f"{cls.__name__}.identity_fields must be a tuple for immutability."
            )

    # ------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------
    @classmethod
    def create(cls, **kwargs):
        """
        Contributor-safe creation:
        - canonicalizes fields
        - computes identity + checksum
        - prevents accidental overwrites
        """
        instance = cls(**kwargs)
        instance = instance.canonicalize()
        instance._compute_checksum()
        instance.save()
        return instance

    # ------------------------------------------------------------
    # Canonicalization hook
    # ------------------------------------------------------------
    def canonicalize(self):
        """
        Subclasses may override to normalize fields:
        - trim whitespace
        - normalize hyphens
        - uppercase codes
        - collapse double spaces
        """
        return self

    # ------------------------------------------------------------
    # Identity + hashing
    # ------------------------------------------------------------
    @property
    def identity_string(self):
        """
        Deterministic identity string based on identity_fields.
        Order matters. Missing fields raise errors.
        """
        parts = []
        for field in self.identity_fields:
            value = getattr(self, field, None)
            if value is None:
                raise ValueError(
                    f"Identity field '{field}' is missing on {self.__class__.__name__}"
                )
            parts.append(f"{field}={value}")
        return "|".join(parts)

    def _compute_checksum(self):
        """
        Hash of the identity_string only.
        Status changes do NOT affect checksum.
        """
        self.checksum = hash_string(self.identity_string)

    # ------------------------------------------------------------
    # Friendly name
    # ------------------------------------------------------------
    @property
    def friendly_name(self):
        """
        Human-readable name based on friendly_name_template.
        """
        if not self.friendly_name_template:
            return self.identity_string
        return self.friendly_name_template.format(**self.__dict__)

    # ------------------------------------------------------------
    # Save override (identity immutability)
    # ------------------------------------------------------------
    def save(self, *args, **kwargs):
        if self.pk is not None:
            existing = self.__class__.objects.get(pk=self.pk)
            if existing.identity_string != self.identity_string:
                raise ValueError(
                    f"Identity fields are immutable for {self.__class__.__name__}. "
                    f"Attempted change from '{existing.identity_string}' "
                    f"to '{self.identity_string}'."
                )
        super().save(*args, **kwargs)
