class PromotionResult:
    def __init__(self, created, updated, canonical_object, warnings=None):
        self.created = created
        self.updated = updated
        self.canonical_object = canonical_object
        self.warnings = warnings or []
