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
# Import Helper Models
# -----------------------------
from .bridge_player_team import BridgePlayerTeam

# -----------------------------
# Import Checklist Ingest Models
# -----------------------------
from .checklist_upload import ChecklistUpload

__all__ = [
    "DimSet", "DimCard", "DimParallel", "DimGrade", "DimUsers", "FactSessions",
    "DimParallelSet", "DimCardParallel",
    "FactCardEvents", "FactInventory", "FactInventoryDetail",
    "FactPlayerMaster", "FactTeamMaster", "FactUsersOTP",
    "BridgePlayerTeam", "ChecklistUpload",
    "BaseIdentity", "SoftDeleteMixin", "ActiveManager"
]
