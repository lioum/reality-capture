# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue
from reality_apis.RModS.production_specifications import Export, Format, _export_options_from_json_file
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
                specifications.outputs.exports = _export_options_from_json_file(specifications_json)
            if "referenceModel" in specifications_json["outputs"]:
                reference_model = ReferenceModel()
                reference_model.reference_model_path = specifications_json["outputs"]["referenceModel"]["path"]
                specifications.outputs.reference_model = reference_model

            if "options" in specifications_json:
                if "workspace" in specifications_json["options"]:
                    specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")


