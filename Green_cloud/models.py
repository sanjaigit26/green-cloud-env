from pydantic import BaseModel
from typing import List, Dict, Optional

class EnergySource(BaseModel):
    name: str
    carbon_intensity: float
    cost: float
    availability: float

class Region(BaseModel):
    name: str
    capacity: int
    energy_mix: Dict[str, float]

class Job(BaseModel):
    id: int
    compute_required: int
    deadline: int
    assigned: bool = False
    assigned_region: Optional[str] = None

class Observation(BaseModel):
    time: int
    jobs: List[Job]
    regions: List[Region]
    energy_sources: Dict[str, EnergySource]

class Action(BaseModel):
    job_id: int
    region: str
    action_type: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict = {}
