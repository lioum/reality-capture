# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os


class ReferenceModelType(Enum):
    Orthophoto = 0
    Complete = 1

class TilingMode(Enum):
    NoTiling = 0
    RegularPlanarGrid = 1
    RegularVolumetricGrid = 2
    Adaptive = 3

class GeometricPrecision(Enum):
    Draft = 0
    Medium = 1
    High = 2
    Extra = 3
    Ultra = 4

class PairSelection(Enum):
    Generic = 0
    StructuredAerial = 1
    RegionOfInterest = 2

class PhotoUsedForGeometry(Enum):
    ExcludeThermal = 0
    IncludeThermal = 1
    NoPhoto = 2

class HoleFilling(Enum):
    SmallHoles = 0
    AllHoles = 1

class Simplification(Enum):
    Standard = 0
    PlanarRelative = 1
    PlanarAbsolute = 2

class ColorCorrection(Enum):
    NoCorrection = 0
    Standard = 1
    StandardWithThermal = 2
    BlockWise = 3
    BlockWiseWithThermal = 4

class UntexturedRepresentation(Enum):
    InpaintingCompletion = 0
    UniformColor = 1

class TextureSource(Enum):
    PhotosFirst = 0
    PointCloudsFirst = 1
    Smart = 2

class ReferenceModel:
    def __init__(self) -> None:
        self.reference_model_path: str = None
        self.options: ReferenceModelOptions = None

class Point3d:
    def __init__(self, x=0, y=0, c=0) -> None:
        self.x = x
        self.y = y
        self.z = z

class ReferenceModelOptions:
    def __init__(self) -> None:
        self.ref_model_type: ReferenceModelType = None
        self.tiling_mode: TilingMode = None
        self.tiling_value: float = None
        self.tilingOrigin: Point3d = None
        self.discard_empty_tiles: bool = None
        self.srs: str = None
        self.geometric_precision: GeometricPrecision = None
        self.pair_selection: PairSelection = None
        self.photo_used_for_geometry: PhotoUsedForGeometry = None
        self.hole_filling: HoleFilling = None
        self.simplification: Simplification = None
        self.planar_simplification_tolerance: float = None
        self.color_correction: ColorCorrection = None
        self.untextured_representation: UntexturedRepresentation = None
        self.untextured_color: str = None
        self.texture_source = None #TextureSource
        self.ortho_resolution: float = None
        self.geometry_resolution_limit: float = None
        self.texture_resolution_limit: float = None

class TilingSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "Tiling"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""
            self.preset: str = None

    class Outputs:
        def __init__(self) -> None:
            self.reference_model: ReferenceModel = ReferenceModel()

    class Options:
        def __init__(self) -> None:
            self.workspace: str = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[TilingSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=TilingSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=TilingSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = TilingSpecifications()
        try:
            if "Scene" in specifications_json["Inputs"]:
                specifications.inputs.scene = specifications_json["Inputs"]["Scene"]

            if "ReferenceModel" in specifications_json["Outputs"]:
                reference_model = ReferenceModel()
                reference_model.reference_model_path = specifications_json["Outputs"]["ReferenceModel"]["Path"]
                specifications.outputs.reference_model = reference_model

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


