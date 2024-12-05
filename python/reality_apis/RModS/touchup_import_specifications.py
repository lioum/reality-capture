# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations

from reality_apis.utils import ReturnValue

import json
import os

class TouchUpImportSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()

    def get_type(self) -> str:
        return "TouchUpImport"

    class Inputs:
        def __init__(self) -> None:
            self.touchup_data: str = ""
            self.reference_model: str = ""
            self.exports_to_amend: list[str] = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[TouchUpImportSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=TouchUpImportSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=TouchUpImportSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = TouchUpImportSpecifications()

        try:
            specifications.inputs.touchup_data = specifications_json["inputs"]["touchUpData"]
            specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "exportsToAmend" in specifications_json["inputs"]:
                for export_to_amend in specifications_json["inputs"]["exportsToAmend"]:
                    specifications.inputs.exports_to_amend.append(export_to_amend)

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")