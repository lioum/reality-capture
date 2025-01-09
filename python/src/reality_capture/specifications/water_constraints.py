from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class WaterConstraintsInputs(BaseModel):
    scene: str = Field(description="Reality data id of ContextScene")
    reference_model: str = Field(alias="referenceModel", description="Reality data id of Reference Model")
    water_detector: Optional[str] = Field(alias="waterDetector", description="Path to water detector")


class WaterConstraintsOptions(BaseModel):
    force_horizontal: Optional[bool] = Field(None, alias="forceHorizontal",
                                             description="Force constraints to be horizontal")


class WaterConstraintsOutputsCreate(Enum):
    CONSTRAINTS = "constraints"


class WaterConstraintsOutputs(BaseModel):
    constraints: str = Field(description="Reality data id of output constraints")


class WaterConstraintsSpecificationsCreate(BaseModel):
    inputs: WaterConstraintsInputs = Field(description="Inputs")
    outputs: list[WaterConstraintsOutputsCreate] = Field(description="Outputs")
    options: WaterConstraintsOptions = Field(description="Options")


class WaterConstraintsSpecifications(BaseModel):
    inputs: WaterConstraintsInputs = Field(description="Inputs")
    outputs: WaterConstraintsOutputs = Field(description="Outputs")
    options: WaterConstraintsOptions = Field(description="Options")
