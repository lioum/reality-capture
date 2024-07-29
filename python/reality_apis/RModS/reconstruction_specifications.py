# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue
from reality_apis.RModS.production_specifications import Export, Format
from reality_apis.RModS.tiling_specifications import ReferenceModel

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
            self.exports: list[Export] = []
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
                    export.export_path = exports_json["path"]
                    if exports_json["format"] == "3MX":
                        export.format = Format.ThreeMX
                    if exports_json["format"] == "3SM":
                        export.format = Format.ThreeSM
                    if exports_json["format"] == "Cesium3DTiles":
                        export.format = Format.Cesium3DTiles
                    if exports_json["format"] == "OSGB":
                        export.format = Format.OSGB
                    if exports_json["format"] == "SpacEyes":
                        export.format = Format.SpacEyes
                    if exports_json["format"] == "OBJ":
                        export.format = Format.OBJ
                    if exports_json["format"] == "S3C":
                        export.format = Format.S3C
                    if exports_json["format"] == "I3S":
                        export.format = Format.I3S
                    if exports_json["format"] == "LodTree":
                        export.format = Format.LodTree
                    if exports_json["format"] == "Collada":
                        export.format = Format.Collada
                    if exports_json["format"] == "OCP":
                        export.format = Format.OCP
                    if exports_json["format"] == "KML":
                        export.format = Format.KML
                    if exports_json["format"] == "DGN":
                        export.format = Format.DGN
                    if exports_json["format"] == "SuperMap":
                        export.format = Format.SuperMap
                    if exports_json["format"] == "Las":
                        export.format = Format.Las
                    if exports_json["format"] == "POD":
                        export.format = Format.POD
                    if exports_json["format"] == "Ply":
                        export.format = Format.Ply
                    if exports_json["format"] == "OPC":
                        export.format = Format.OPC
                    if exports_json["format"] == "OrthophotoDSM":
                        export.format = Format.OrthophotoDSM
                    if exports_json["format"] == "Touchup":
                        export.format = Format.Touchup
                    exports.append(export)
                specifications.outputs.exports = exports

            if "referenceModel" in specifications_json["outputs"]:
                reference_model = ReferenceModel()
                reference_model.reference_model_path = specifications_json["outputs"]["referenceModel"]["path"]
                specifications.outputs.reference_model = reference_model

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


