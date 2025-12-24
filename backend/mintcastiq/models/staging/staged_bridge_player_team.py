from django.db import models
from mintcastiq.models.fact_player_master import FactPlayerMaster
from mintcastiq.models.fact_team_master import FactTeamMaster

class StagedPlayerTeam(models.Model):
    player = models.ForeignKey(FactPlayerMaster, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(FactTeamMaster, null=True, on_delete=models.SET_NULL)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
