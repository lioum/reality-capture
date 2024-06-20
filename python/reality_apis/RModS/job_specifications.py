# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import TypeVar, NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os

class JobType(Enum):
    NONE = "not recognized"
    Reconstruction = "Reconstruction"

class Format(Enum):
    ThreeMX = 0
    #TODO : add other formats
    """ThreeSM = 1
    Cesium3DTiles = 2
    OSGB = 3
    SpacEyes = 4
    OBJ = 5
    S3C = 6
    I3S = 7
    LodTree = 8
    Collada = 9
    OCP = 10
    KML = 11
    DGN = 12
    SuperMap = 13
    Las = 14
    POD = 15
    Ply = 16
    OPC = 17
    OrthophotoDSM = 18
    Touchup = 19"""

class ColorSource(Enum):
    Visible = 0
    Thermal = 1
    Resolution = 2

class ThermalUnit(Enum):
    Absolute = 0
    Celsius = 1
    Fahrenheit = 2

class LodScope(Enum):
    TileWise = 0
    AcrossTiles = 1

class Options3MX:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = 0
        self.texture_color_source_res_min: float = 0
        self.texture_color_source_res_max: float = 0
        self.texture_color_source_thermal_unit: ThermalUnit = 0
        self.texture_color_source_thermal_max: float = 0
        self.texture_color_source_thermal_min: float = 0
        self.srs: str = ""
        self.srs_origin: str = ""
        self.lod_scope: LODScope = 0
        self.generate_web_app: bool = False

class Export:
    def __init__(self) -> None:
        self.format: Format = 0
        self.export_path: str = ""
        self.options_3MX: Options3MX = Options3MX()

class ReconstructionSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "Reconstruction"

    class Inputs:
        def __init__(self) -> None:
            self.oriented_photos: str = ""
            #TODO : other inputs

    class Outputs:
        def __init__(self) -> None:
            self.exports: list[Export] = []
            #TODO : do other outputs

    class Options:
        def __init__(self) -> None:
            self.workspace: str = ""

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[ReconstructionSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=ReconstructionSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=ReconstructionSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = ReconstructionSpecifications()
        try:
            specifications.inputs.oriented_photos = specifications_json["Inputs"]["OrientedPhotos"]

            exports = []
            for exports_json in specifications_json["Outputs"]["Exports"]:
                export = Export()
                export.export_path = exports_json["Path"]
                if exports_json["Format"] == "3MX":
                    export.format = Format.ThreeMX
                exports.append(export)
            specifications.outputs.exports = exports
        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")

class CalibrationSpecifications:
    def __init__(self) -> None:
        self.options = self.Options()

    class Outputs:
        def __init__(self) -> None:
            self.place_holder: str
            #TODO : do other outputs

Specifications = TypeVar(
    "Specifications",
    ReconstructionSpecifications,
    CalibrationSpecifications
)

