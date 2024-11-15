# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations

from reality_apis.utils import ReturnValue

import json
import os

class ImportPCSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()

    def get_type(self) -> str:
        return "ImportPC"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""

    class Outputs:
        def __init__(self) -> None:
            self.scan_collection: str = ""

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[ImportPCSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=ImportPCSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=ImportPCSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = ImportPCSpecifications()

        try:
            specifications.inputs.scene = specifications_json["inputs"]["scene"]

            specifications.outputs.scan_collection = specifications_json["outputs"]["scanCollection"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")