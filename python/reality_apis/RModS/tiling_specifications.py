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
    def __init__(self, x=0, y=0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z

class ReferenceModelOptions:
    def __init__(self) -> None:
        self.ref_model_type: ReferenceModelType = None
        self.tiling_mode: TilingMode = None
        self.tiling_value: float = None
        self.tiling_origin: Point3d = None
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
        self.texture_source: TextureSource = None
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
            specifications.inputs.scene = specifications_json["inputs"]["scene"]
            if "preset" in specifications_json["inputs"]:
                specifications.inputs.preset = specifications_json["inputs"]["preset"]

            if "referenceModel" in specifications_json["outputs"]:
                reference_model = ReferenceModel()
                reference_model.reference_model_path = specifications_json["outputs"]["referenceModel"]["referenceModelPath"]

                reference_model.options = ReferenceModelOptions()
                if "refModelType" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.ref_model_type = ReferenceModelType[specifications_json["outputs"]["referenceModel"]["options"]["refModelType"]]
                if "tilingMode" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.tiling_mode = TilingMode[specifications_json["outputs"]["referenceModel"]["options"]["tilingMode"]]
                if "tilingValue" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.tiling_value = specifications_json["outputs"]["referenceModel"]["options"]["tilingValue"]
                if "tilingOrigin" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.tiling_origin = Point3d[specifications_json["outputs"]["referenceModel"]["options"]["tilingOrigin"]]
                if "discardEmptyTiles" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.discard_empty_tiles = specifications_json["outputs"]["referenceModel"]["options"]["discardEmptyTiles"]
                if "srs" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.srs = specifications_json["outputs"]["referenceModel"]["options"]["srs"]
                if "geometricPrecision" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.geometric_precision = GeometricPrecision[specifications_json["outputs"]["referenceModel"]["options"]["geometricPrecision"]]
                if "pairSelection" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.pair_selection = PairSelection[specifications_json["outputs"]["referenceModel"]["options"]["pairSelection"]]
                if "photoUsedForGeometry" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.photo_used_for_geometry = PhotoUsedForGeometry[specifications_json["outputs"]["referenceModel"]["options"]["photoUsedForGeometry"]]
                if "holeFilling" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.hole_filling = HoleFilling[specifications_json["outputs"]["referenceModel"]["options"]["holeFilling"]]
                if "simplification" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.simplification = Simplification[specifications_json["outputs"]["referenceModel"]["options"]["simplification"]]
                if "planarSimplificationTolerance" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.planar_simplification_tolerance = specifications_json["outputs"]["referenceModel"]["options"]["planarSimplificationTolerance"]
                if "colorCorrection" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.color_correction = ColorCorrection[specifications_json["outputs"]["referenceModel"]["options"]["colorCorrection"]]
                if "untexturedRepresentation" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.untextured_representation = UntexturedRepresentation[specifications_json["outputs"]["referenceModel"]["options"]["untexturedRepresentation"]]
                if "untexturedColor" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.untextured_color = specifications_json["outputs"]["referenceModel"]["options"]["untexturedColor"]
                if "textureSource" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.texture_source = TextureSource[specifications_json["outputs"]["referenceModel"]["options"]["textureSource"]]
                if "orthoResolution" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.ortho_resolution = specifications_json["outputs"]["referenceModel"]["options"]["orthoResolution"]
                if "geometryResolutionLimit" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.geometry_resolution_limit = specifications_json["outputs"]["referenceModel"]["options"]["geometryResolutionLimit"]
                if "textureResolutionLimit" in specifications_json["outputs"]["referenceModel"]["options"]:
                    reference_model.options.texture_resolution_limit = specifications_json["outputs"]["referenceModel"]["options"]["textureResolutionLimit"]

                specifications.outputs.reference_model = reference_model

            if "workspace" in specifications_json["options"]:
                specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


