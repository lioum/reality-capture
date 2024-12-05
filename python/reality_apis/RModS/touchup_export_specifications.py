# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os

class TouchFormat(Enum):
    OBJ = 0
    DGN = 1

class Level(Enum):
    Geometry = 0
    GeometryAndTexture = 1

class TouchUpExportSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "TouchUpExport"

    class Inputs:
        def __init__(self) -> None:
            self.reference_model: str = ""
            self.tiles_to_touchup: list[str] = None

    class Outputs:
        def __init__(self) -> None:
            self.touchup_data: str = ""

    class Options:
        def __init__(self) -> None:
            self.format: TouchFormat = None
            self.level: Level = None
            self.srs: str = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[TouchUpExportSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=TouchUpExportSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=TouchUpExportSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = TouchUpExportSpecifications()

        try:
            specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "tilesToTouchUp" in specifications_json["inputs"]:
                for tile in specifications_json["inputs"]["tilesToTouchUp"]:
                    specifications.inputs.tiles_to_touchup.append(tile)

            specifications.outputs.touchup_data = specifications_json["outputs"]["touchUpData"]

            if "options" in specifications_json:
                if "format" in specifications_json["options"]:
                    specifications.options.format = specifications_json["options"]["format"]
                if "level" in specifications_json["options"]:
                    specifications.options.level = specifications_json["options"]["level"]
                if "srs" in specifications_json["options"]:
                    specifications.options.srs = specifications_json["options"]["srs"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")