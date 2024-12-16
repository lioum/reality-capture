# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue
from reality_apis.RModS.production_specifications import Export, Format, _export_options_from_json_file
from reality_apis.RModS.tiling_specifications import (ReferenceModel, ReferenceModelOptions, TilingMode, Point3d, HoleFilling,
                                                      TextureSource, Simplification, PhotoUsedForGeometry, PairSelection,
                                                      UntexturedRepresentation, ColorCorrection, GeometricPrecision, ReferenceModelType)

import json
import os

class ReconstructionSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "Reconstruction"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""
            self.reference_model = None
            self.preset: str = None

    class Outputs:
        def __init__(self) -> None:
            self.exports: list[Export] = None
            self.reference_model: ReferenceModel = None

    class Options:
        def __init__(self) -> None:
            self.workspace: str = None

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
            specifications.inputs.scene = specifications_json["inputs"]["scene"]
            if "referenceModel" in specifications_json["inputs"]:
                specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "preset" in specifications_json["inputs"]:
                specifications.inputs.preset = specifications_json["inputs"]["preset"]

            if "exports" in specifications_json["outputs"]:
                specifications.outputs.exports = _export_options_from_json_file(specifications_json)
            if "referenceModel" in specifications_json["outputs"]:
                reference_model = ReferenceModel()
                reference_model.reference_model_path = specifications_json["outputs"]["referenceModel"]["referenceModelPath"]
                if "options" in specifications_json["outputs"]["referenceModel"]:
                    reference_model.options = ReferenceModelOptions()
                    if "refModelType" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.ref_model_type = ReferenceModelType[
                            specifications_json["outputs"]["referenceModel"]["options"]["refModelType"]]
                    if "tilingMode" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.tiling_mode = TilingMode[
                            specifications_json["outputs"]["referenceModel"]["options"]["tilingMode"]]
                    if "tilingValue" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.tiling_value = \
                        specifications_json["outputs"]["referenceModel"]["options"]["tilingValue"]
                    if "tilingOrigin" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.tiling_origin = Point3d[
                            specifications_json["outputs"]["referenceModel"]["options"]["tilingOrigin"]]
                    if "discardEmptyTiles" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.discard_empty_tiles = \
                        specifications_json["outputs"]["referenceModel"]["options"]["discardEmptyTiles"]
                    if "srs" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.srs = specifications_json["outputs"]["referenceModel"]["options"]["srs"]
                    if "geometricPrecision" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.geometric_precision = GeometricPrecision[
                            specifications_json["outputs"]["referenceModel"]["options"]["geometricPrecision"]]
                    if "pairSelection" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.pair_selection = PairSelection[
                            specifications_json["outputs"]["referenceModel"]["options"]["pairSelection"]]
                    if "photoUsedForGeometry" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.photo_used_for_geometry = PhotoUsedForGeometry[
                            specifications_json["outputs"]["referenceModel"]["options"]["photoUsedForGeometry"]]
                    if "holeFilling" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.hole_filling = HoleFilling[
                            specifications_json["outputs"]["referenceModel"]["options"]["holeFilling"]]
                    if "simplification" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.simplification = Simplification[
                            specifications_json["outputs"]["referenceModel"]["options"]["simplification"]]
                    if "planarSimplificationTolerance" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.planar_simplification_tolerance = \
                        specifications_json["outputs"]["referenceModel"]["options"]["planarSimplificationTolerance"]
                    if "colorCorrection" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.color_correction = ColorCorrection[
                            specifications_json["outputs"]["referenceModel"]["options"]["colorCorrection"]]
                    if "untexturedRepresentation" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.untextured_representation = UntexturedRepresentation[
                            specifications_json["outputs"]["referenceModel"]["options"]["untexturedRepresentation"]]
                    if "untexturedColor" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.untextured_color = \
                        specifications_json["outputs"]["referenceModel"]["options"]["untexturedColor"]
                    if "textureSource" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.texture_source = TextureSource[
                            specifications_json["outputs"]["referenceModel"]["options"]["textureSource"]]
                    if "orthoResolution" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.ortho_resolution = \
                        specifications_json["outputs"]["referenceModel"]["options"]["orthoResolution"]
                    if "geometryResolutionLimit" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.geometry_resolution_limit = \
                        specifications_json["outputs"]["referenceModel"]["options"]["geometryResolutionLimit"]
                    if "textureResolutionLimit" in specifications_json["outputs"]["referenceModel"]["options"]:
                        reference_model.options.texture_resolution_limit = \
                        specifications_json["outputs"]["referenceModel"]["options"]["textureResolutionLimit"]
                specifications.outputs.reference_model = reference_model

            if "options" in specifications_json:
                if "workspace" in specifications_json["options"]:
                    specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


