print("LOADING MODELS INIT")
print("DimSet imported?", "DimSet" in globals())

# -----------------------------
# Import Managers
# -----------------------------
from .managers.active_manager import ActiveManager

# -----------------------------
# Import Base classes
# -----------------------------
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

# ----------------------------- 
# Import Dimension Models   
# -----------------------------
from .dim_set import DimSet
from .dim_parallel import DimParallel
from .dim_card import DimCard   
from .dim_grade import DimGrade  
from .dim_users import DimUsers    
from .fact_sessions import FactSessions    

# ----------------------------- 
# Import Glue Models (NEW)
# -----------------------------
from .dim_parallel_set import DimParallelSet
from .dim_card_parallel import DimCardParallel

# ----------------------------- 
# Import Fact Models    
# -----------------------------
from .fact_card_events import FactCardEvents   
from .fact_inventory import FactInventory
from .fact_inventory_detail import FactInventoryDetail
from .fact_player_master import FactPlayerMaster
from .fact_team_master import FactTeamMaster
from .fact_users_otp import FactUsersOTP

# -----------------------------
# Import Staging Models
# -----------------------------
from .staging.staged_bridge_player_team import StagedPlayerTeam
from .staging.staged_card_event import StagedCardEvent
from .staging.staged_card import StagedCard
from .staging.staged_inventory_detail import StagedInventoryDetail
from .staging.staged_inventory import StagedInventory
from .staging.staged_parallel import StagedParallel
from .staging.staged_player_master import StagedPlayerMaster
from .staging.staged_set import StagedSet
from .staging.staged_team_master import StagedTeamMaster

# -----------------------------
# Import Helper Models
# -----------------------------
from .bridge_player_team import BridgePlayerTeam

# -----------------------------
# Import Checklist Ingest Models
# -----------------------------
from .checklist_upload import ChecklistUpload
from .staging.staging_checklist_row import StagingChecklistRow
from .fact_checklist_entry import FactChecklistEntry

__all__ = [
    "DimSet", "DimCard", "DimParallel", "DimGrade", "DimUsers", "FactSessions",
    "DimParallelSet", "DimCardParallel",
    "FactCardEvents", "FactInventory", "FactInventoryDetail",
    "FactPlayerMaster", "FactTeamMaster", "FactUsersOTP",
    "BridgePlayerTeam", "ChecklistUpload", "StagingChecklistRow", "FactChecklistEntry",
    "BaseIdentity", "SoftDeleteMixin", "ActiveManager",
    "StagedPlayerTeam", "StagedCardEvent", "StagedCard",
    "StagedInventoryDetail", "StagedInventory", "StagedParallel",
    "StagedPlayerMaster", "StagedSet", "StagedTeamMaster"
]
