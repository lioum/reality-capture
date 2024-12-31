# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations

from reality_apis.utils import ReturnValue

import json
import os


class WaterConstraintsSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "WaterConstraints"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""
            self.reference_model: str = ""
            self.water_detector: str = None

    class Outputs:
        def __init__(self) -> None:
            self.constraints: str = ""

    class Options:
        def __init__(self) -> None:
            self.force_horizontal: bool = None
            self.workspace: str = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[WaterConstraintsSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=WaterConstraintsSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=WaterConstraintsSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = WaterConstraintsSpecifications()

        try:
            specifications.inputs.scene = specifications_json["inputs"]["scene"]
            specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "waterDetector" in specifications_json["inputs"]:
                specifications.inputs.water_detector = specifications_json["inputs"]["waterDetector"]

            specifications.outputs.constraints = specifications_json["outputs"]["constraints"]

            if "options" in specifications_json:
                if "forceHorizontal" in specifications_json["options"]:
                    specifications.options.force_horizontal = specifications_json["options"]["forceHorizontal"]
                if "workspace" in specifications_json["options"]:
                    specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")