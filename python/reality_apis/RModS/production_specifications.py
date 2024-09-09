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

class LODScope(Enum):
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


def _texture_color_source_from_json(options, options_json):
    if "textureColorSource" in options_json:
        options.texture_color_source = ColorSource[options_json["textureColorSource"]]
    if "textureColorSourceResMin" in options_json:
        options.texture_color_source_res_min = options_json["textureColorSourceResMin"]
    if "textureColorSourceResMax" in options_json:
        options.texture_color_source_res_max = options_json["textureColorSourceResMax"]
    if "textureColorSourceThermalUnit" in options_json:
        options.texture_color_source_thermal_unit = ThermalUnit[options_json["textureColorSourceThermalUnit"]]
    if "textureColorSourceThermalMin" in options_json:
        options.texture_color_source_thermal_min = options_json["textureColorSourceThermalMin"]
    if "textureColorSourceThermalMax" in options_json:
        options.texture_color_source_thermal_max = options_json["textureColorSourceThermalMax"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "generateWebApp" in options_json:
            self.generate_web_app = options_json["generateWebApp"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "compress" in options_json:
            self.compress = CesiumCompression[options_json["compress"]]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODScope[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "disableLighting" in options_json:
            self.disable_lighting = options_json["disableLighting"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "maximumTextureSize" in options_json:
            self.maximum_texture_size = options_json["maximumTextureSize"]
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]
        if "doublePrecision" in options_json:
            self.double_precision = options_json["doublePrecision"]


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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "version" in options_json:
            self.version = I3SVersion[options_json["version"]]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "heightOffset" in options_json:
            self.height_offset = options_json["heightOffset"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "lodType" in options_json:
            self.lod_type = LODType[options_json["lodType"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "srsOrigin" in options_json:
            self.srs_origin = options_json["srsOrigin"]

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

    def from_json(self, options_json):
        _texture_color_source_from_json(self, options_json)
        if "lodScope" in options_json:
            self.lod_scope = LODScope[options_json["lodScope"]]
        if "srs" in options_json:
            self.srs = options_json["srs"]

class OptionsLas:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.compress: LasCompression = None
        self.merge_point_clouds: bool = None
        self.texture_color_source: ColorSource = None

    def from_json(self, options_json):
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "samplingStrategy" in options_json:
            self.sampling_strategy = SamplingStrategy[options_json["samplingStrategy"]]
        if "samplingDistance" in options_json:
            self.sampling_distance = options_json["samplingDistance"]
        if "compress" in options_json:
            self.compress = LasCompression[options_json["compress"]]
        if "mergePointClouds" in options_json:
            self.merge_point_clouds = options_json["mergePointClouds"]
        if "textureColorSource" in options_json:
            self.texture_color_source = ColorSource[options_json["textureColorSource"]]

class OptionsPod:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.texture_color_source: ColorSource = None

    def from_json(self, options_json):
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "samplingStrategy" in options_json:
            self.sampling_strategy = SamplingStrategy[options_json["samplingStrategy"]]
        if "samplingDistance" in options_json:
            self.sampling_distance = options_json["samplingDistance"]
        if "textureColorSource" in options_json:
            self.texture_color_source = ColorSource[options_json["textureColorSource"]]

class OptionsPly:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.merge_point_clouds: bool = None
        self.include_normals: bool = None
        self.texture_color_source: ColorSource = None

    def from_json(self, options_json):
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "samplingStrategy" in options_json:
            self.sampling_strategy = SamplingStrategy[options_json["samplingStrategy"]]
        if "samplingDistance" in options_json:
            self.sampling_distance = options_json["samplingDistance"]
        if "mergePointClouds" in options_json:
            self.merge_point_clouds = options_json["mergePointClouds"]
        if "includeNormals" in options_json:
            self.include_normals = options_json["includeNormals"]
        if "textureColorSource" in options_json:
            self.texture_color_source = ColorSource[options_json["textureColorSource"]]

class OptionsOpc:
    def __init__(self) -> None:
        self.srs: str = None
        self.sampling_strategy: SamplingStrategy = None
        self.sampling_distance: float = None
        self.texture_color_source: ColorSource = None

    def from_json(self, options_json):
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "samplingStrategy" in options_json:
            self.sampling_strategy = SamplingStrategy[options_json["samplingStrategy"]]
        if "samplingDistance" in options_json:
            self.sampling_distance = options_json["samplingDistance"]
        if "textureColorSource" in options_json:
            self.texture_color_source = ColorSource[options_json["textureColorSource"]]

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
        self.no_data_transparency: bool = None

    def from_json(self, options_json):
        if "srs" in options_json:
            self.srs = options_json["srs"]
        if "samplingStrategy" in options_json:
            self.sampling_strategy = SamplingStrategy[options_json["samplingStrategy"]]
        if "extentFile" in options_json:
            self.extent_file = options_json["extentFile"]
        if "projectionMode" in options_json:
            self.projection_mode = ProjectionMode[options_json["projectionMode"]]
        if "mergeParts" in options_json:
            self.merge_parts = options_json["mergeParts"]
        if "orthoFormat" in options_json:
            self.ortho_format = OrthoFormat[options_json["orthoFormat"]]
        if "noDataColor" in options_json:
            self.no_data_color = options_json["noDataColor"]
        if "colorSource" in options_json:
            self.color_source = OrthoColorSource[options_json["colorSource"]]
        if "dsmFormat" in options_json:
            self.dsm_format = DSMFormat[options_json["dsmFormat"]]
        if "noDataValue" in options_json:
            self.no_data_value = options_json["noDataValue"]
        if "noDataTransparency" in options_json:
            self.no_data_transparency = options_json["noDataTransparency"]


class OptionsTouchup:
    def __init__(self) -> None:
        self.format: TouchupFormat = None
        self.texture_color_source: ColorSource = None
        self.maximum_texture_size: int = None

    def from_json(self, options_json):
        if "format" in options_json:
            self.format = TouchupFormat[options_json["format"]]
        if "textureColorSource" in options_json:
            self.texture_color_source = ColorSource[options_json["textureColorSource"]]
        if "maximumTextureSize" in options_json:
            self.maximum_texture_size = options_json["maximumTextureSize"]


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

        self.options_orthodsm: OptionsOrthoDSM = OptionsOrthoDSM()

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
            self.preset = None

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
            if "scene" in specifications_json["inputs"]:
                specifications.inputs.scene = specifications_json["inputs"]["scene"]
            if "referenceModel" in specifications_json["inputs"]:
                specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "preset" in specifications_json["inputs"]:
                specifications.inputs.preset = specifications_json["inputs"]["preset"]

            if "exports" in specifications_json["outputs"]:
                exports = []
                for exports_json in specifications_json["outputs"]["exports"]:
                    export = Export()
                    export.export_path = exports_json["exportPath"]

                    if exports_json["format"] == "3MX":
                        export.format = Format.ThreeMX
                        if "options3MX" in exports_json:
                            options = Options3MX()
                            options.from_json(exports_json["options3MX"])
                            export.options_3mx = options
                    elif exports_json["format"] == "3SM":
                        export.format = Format.ThreeSM
                        if "options3SM" in exports_json:
                            options = Options3SM()
                            options.from_json(exports_json["options3SM"])
                            export.options_3sm = options
                    elif exports_json["format"] == "Cesium3DTiles":
                        export.format = Format.Cesium3DTiles
                        if "optionsCesium" in exports_json:
                            options = OptionsCesium()
                            options.from_json(exports_json["optionsCesium"])
                            export.options_cesium = options
                    elif exports_json["format"] == "OSGB":
                        export.format = Format.OSGB
                        if "optionsOSGB" in exports_json:
                            options = OptionsOSGB()
                            options.from_json(exports_json["optionsOSGB"])
                            export.options_osgb = options
                    elif exports_json["format"] == "SpacEyes":
                        export.format = Format.SpacEyes
                        if "optionsSpacEyes" in exports_json:
                            options = OptionsSpacEyes()
                            options.from_json(exports_json["optionsSpacEyes"])
                            export.options_spac_eyes = options
                    elif exports_json["format"] == "OBJ":
                        export.format = Format.OBJ
                        if "optionsObj" in exports_json:
                            options = OptionsObj()
                            options.from_json(exports_json["optionsObj"])
                            export.options_obj = options
                    elif exports_json["format"] == "S3C":
                        export.format = Format.S3C
                        if "optionsS3C" in exports_json:
                            options = OptionsS3C()
                            options.from_json(exports_json["optionsS3C"])
                            export.options_s3c = options
                    elif exports_json["format"] == "I3S":
                        export.format = Format.I3S
                        if "optionsI3S" in exports_json:
                            options = OptionsI3S()
                            options.from_json(exports_json["optionsI3S"])
                            export.options_i3s = options
                    elif exports_json["format"] == "LodTree":
                        export.format = Format.LodTree
                        if "optionsLodTree" in exports_json:
                            options = OptionsLodTreeExport()
                            options.from_json(exports_json["optionsLodTree"])
                            export.options_lod_tree = options
                    elif exports_json["format"] == "Collada":
                        export.format = Format.Collada
                        if "optionsCollada" in exports_json:
                            options = OptionsCollada()
                            options.from_json(exports_json["optionsCollada"])
                            export.options_collada = options
                    elif exports_json["format"] == "OCP":
                        export.format = Format.OCP
                        if "optionsOCP" in exports_json:
                            options = OptionsOCP()
                            options.from_json(exports_json["optionsOCP"])
                            export.options_ocp = options
                    elif exports_json["format"] == "KML":
                        export.format = Format.KML
                        if "optionsKML" in exports_json:
                            options = OptionsKML()
                            options.from_json(exports_json["optionsKML"])
                            export.options_kml = options
                    elif exports_json["format"] == "DGN":
                        export.format = Format.DGN
                        if "optionsDGN" in exports_json:
                            options = OptionsDGN()
                            options.from_json(exports_json["optionsDGN"])
                            export.options_dgn = options
                    elif exports_json["format"] == "SuperMap":
                        export.format = Format.SuperMap
                        if "optionsSuperMap" in exports_json:
                            options = OptionsSuperMap()
                            options.from_json(exports_json["optionsSuperMap"])
                            export.options_supermap = options
                    elif exports_json["format"] == "Las":
                        export.format = Format.Las
                        if "optionsLas" in exports_json:
                            options = OptionsLas()
                            options.from_json(exports_json["optionsLas"])
                            export.options_las = options
                    elif exports_json["format"] == "POD":
                        export.format = Format.POD
                        if "optionsPod" in exports_json:
                            options = OptionsPod()
                            options.from_json(exports_json["optionsPod"])
                            export.options_pod = options
                    elif exports_json["format"] == "Ply":
                        export.format = Format.Ply
                        if "optionsPly" in exports_json:
                            options = OptionsPly()
                            options.from_json(exports_json["optionsPly"])
                            export.options_ply = options
                    elif exports_json["format"] == "OPC":
                        export.format = Format.OPC
                        if "optionsOpc" in exports_json:
                            options = OptionsOpc()
                            options.from_json(exports_json["optionsOpc"])
                            export.options_opc = options
                    elif exports_json["format"] == "OrthophotoDSM":
                        export.format = Format.OrthophotoDSM
                        if "optionsOrthoDSM" in exports_json:
                            options = OptionsOrthoDSM()
                            options.from_json(exports_json["optionsOrthoDSM"])
                            export.options_orthodsm = options
                    elif exports_json["format"] == "Touchup":
                        export.format = Format.Touchup
                        if "optionsTouchup" in exports_json:
                            options = OptionsTouchup()
                            options.from_json(exports_json["optionsTouchup"])
                            export.options_touchup = options
                    exports.append(export)
                specifications.outputs.exports = exports

            if "workspace" in specifications_json["options"]:
                specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


