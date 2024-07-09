# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os

class Format(Enum):
    ThreeMX = 0
    ThreeSM = 1
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
    Touchup = 19

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

class CesiumCompression(Enum):
    NoCompression = 0
    Draco = 1

class LODType(Enum):
    NoneLOD = 0
    Unary = 1
    QuadTree = 2
    Octree = 3
    Adaptive = 4
    BingMaps = 5

class I3SVersion(Enum):
    v1_6 = 0
    v1_8 = 1

class SamplingStrategy(Enum):
    Resolution = 0
    Absolute = 1

class LasCompression(Enum):
    NoCompression = 0
    LAZ = 1

class ProjectionMode(Enum):
    HighestPoint = 0
    LowestPoint = 1

class OrthoFormat(Enum):
    GeoTIFF = 0
    JPEG = 1
    KML_SuperOverlay = 2
    NoFormat = 3

class DSMFormat(Enum):
    GeoTIFF = 0
    XYZ = 1
    ASC = 2
    NoFormat = 3

class OrthoColorSource(Enum):
    Reference3dModelVisible = 0
    OptimizedComputationVisible = 1
    Reference3dModelThermal = 2
    OptimizedComputationThermal = 3

class TouchupFormat(Enum):
    OBJ = 0
    DGN = 1

class TouchupFormat(Enum):
    OBJ = 0
    DGN = 1

class Options3MX:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.srs: str = None
        self.srs_origin: str = None
        self.lod_scope: LODScope = None
        self.generate_web_app: bool = None

class Options3SM:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.srs: str = None
        self.lod_scope: LODScope = None

class OptionsCesium:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.srs: str = None
        self.lod_scope: LODScope = None
        self.compress: CesiumCompression = None

class OptionsOSGB:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.srs_origin: str = None

class OptionsSpacEyes:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.disable_lighting: bool = None

class OptionsObj:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.maximum_texture_size: int = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.srs_origin: str = None
        self.double_precision: bool = None

class OptionsS3C:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.srs: str = None
        self.srs_origin: str = None

class OptionsI3S:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.srs: str = None
        self.version: I3SVersion = None

class OptionsLodTreeExport:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None

class OptionsCollada:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.srs_origin: str = None

class OptionsOCP:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.srs: str = None

class OptionsKML:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.height_offset: float = None

class OptionsDGN:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.lod_type: LODType = None
        self.srs: str = None
        self.srs_origin: str = None

class OptionsSuperMap:
    def __init__(self) -> None:
        self.texture_color_source: ColorSource = None
        self.texture_color_source_res_min: float = None
        self.texture_color_source_res_max: float = None
        self.texture_color_source_thermal_unit: ThermalUnit = None
        self.texture_color_source_thermal_min: float = None
        self.texture_color_source_thermal_max: float = None
        self.lod_scope: LODScope = None
        self.srs: str = None

class OptionsLas:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.compress: LasCompression = None
        self.merge_point_clouds: bool = None
        self.texture_color_source: ColorSource = None

class OptionsPod:
    def __init__(self) -> None:
        self.srs: str = None
        self.srs: SamplingStrategy = None
        self.sampling_distance: float = None
        self.texture_color_source: ColorSource = None

class OptionsPly:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.merge_point_clouds: bool = None
        self.include_normals: bool = None
        self.texture_color_source: ColorSource = None

class OptionsOpc:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.texture_color_source: ColorSource = None

class OptionsOrthoDSM:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.extent_file: str = None
        self.projection_mode: ProjectionMode = None
        self.merge_parts: bool = None
        self.ortho_format: OrthoFormat = None
        self.no_data_color: str = None
        self.color_source: OrthoColorSource = None
        self.dsm_format: DSMFormat = None
        self.no_data_value: float = None

class OptionsTouchup:
    def __init__(self) -> None:
        self.format: TouchupFormat = None
        self.texture_color_source: ColorSource = None
        self.maximum_texture_size: int = None


class Export:
    def __init__(self) -> None:
        self.format: Format = None
        self.export_path: str = None
        self.options_3mx: Options3MX = Options3MX()
        self.options_3sm: Options3SM = Options3SM()
        self.options_cesium: OptionsCesium = OptionsCesium()
        self.options_osgb: OptionsOSGB = OptionsOSGB()
        self.options_spac_eyes: OptionsSpacEyes = OptionsSpacEyes()
        self.options_obj: OptionsObj = OptionsObj()
        self.options_s3c: OptionsS3C = OptionsS3C()
        self.options_i3s: OptionsI3S = OptionsI3S()
        self.options_lod_tree: OptionsLodTreeExport = OptionsLodTreeExport()
        self.options_collada: OptionsCollada = OptionsCollada()
        self.options_ocp: OptionsOCP = OptionsOCP()
        self.options_kml: OptionsKML = OptionsKML()
        self.options_dgn: OptionsDGN = OptionsDGN()
        self.options_supermap: OptionsSuperMap = OptionsSuperMap()

        self.options_las: OptionsLas = OptionsLas()
        self.options_pod: OptionsPod = OptionsPod()
        self.options_ply: OptionsPly = OptionsPly()
        self.options_opc: OptionsOpc = OptionsOpc()

        self.options_opc: OptionsOrthoDSM = OptionsOrthoDSM()

        self.options_touchup: OptionsTouchup = OptionsTouchup()

class ProductionSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "Production"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""
            self.reference_model: str = ""

    class Outputs:
        def __init__(self) -> None:
            self.exports: list[Export] = []

    class Options:
        def __init__(self) -> None:
            self.workspace: str = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[ProductionSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=ProductionSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=ProductionSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = ProductionSpecifications()
        try:
            if "Scene" in specifications_json["Inputs"]:
                specifications.inputs.scene = specifications_json["Inputs"]["Scene"]
            if "ReferenceModel" in specifications_json["Inputs"]:
                specifications.inputs.reference_model = specifications_json["Inputs"]["ReferenceModel"]

            if "Exports" in specifications_json["Outputs"]:
                exports = []
                for exports_json in specifications_json["Outputs"]["Exports"]:
                    export = Export()
                    export.export_path = exports_json["Path"]
                    if exports_json["Format"] == "3MX":
                        export.format = Format.ThreeMX
                    if exports_json["Format"] == "3SM":
                        export.format = Format.ThreeSM
                    if exports_json["Format"] == "Cesium3DTiles":
                        export.format = Format.Cesium3DTiles
                    if exports_json["Format"] == "OSGB":
                        export.format = Format.OSGB
                    if exports_json["Format"] == "SpacEyes":
                        export.format = Format.SpacEyes
                    if exports_json["Format"] == "OBJ":
                        export.format = Format.OBJ
                    if exports_json["Format"] == "S3C":
                        export.format = Format.S3C
                    if exports_json["Format"] == "I3S":
                        export.format = Format.I3S
                    if exports_json["Format"] == "LodTree":
                        export.format = Format.LodTree
                    if exports_json["Format"] == "Collada":
                        export.format = Format.Collada
                    if exports_json["Format"] == "OCP":
                        export.format = Format.OCP
                    if exports_json["Format"] == "KML":
                        export.format = Format.KML
                    if exports_json["Format"] == "DGN":
                        export.format = Format.DGN
                    if exports_json["Format"] == "SuperMap":
                        export.format = Format.SuperMap
                    if exports_json["Format"] == "Las":
                        export.format = Format.Las
                    if exports_json["Format"] == "POD":
                        export.format = Format.POD
                    if exports_json["Format"] == "Ply":
                        export.format = Format.Ply
                    if exports_json["Format"] == "OPC":
                        export.format = Format.OPC
                    if exports_json["Format"] == "OrthophotoDSM":
                        export.format = Format.OrthophotoDSM
                    if exports_json["Format"] == "Touchup":
                        export.format = Format.Touchup
                    exports.append(export)
                specifications.outputs.exports = exports

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


