from django.db import models
from .fact_player_master import FactPlayerMaster
from .fact_team_master import FactTeamMaster
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity 

class BridgePlayerTeam(SoftDeleteMixin, BaseIdentity):
    id = models.AutoField(primary_key=True)

    player = models.ForeignKey(FactPlayerMaster, on_delete=models.PROTECT, null=False)
    team = models.ForeignKey(FactTeamMaster, on_delete=models.PROTECT, null=False)

    identity_fields = (
        "player.full_name",
        "team.full_name",
    )

    class Meta:
        db_table = "bridge_player_team"
        constraints = [
            models.UniqueConstraint(
                fields=["player", "team"],
                name="unique_player_team_bridge"
            )
        ]

    
    @property
    def friendly_name(self):
        return f"{self.player.friendly_name} → {self.team.friendly_name}"
