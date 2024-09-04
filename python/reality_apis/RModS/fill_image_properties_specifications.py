# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os


class AltitudeReference(Enum):
    SeaLevel = 0
    WGS84Ellipsoid = 1

class FillImagePropertiesSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "FillImageProperties"

    class Inputs:
        def __init__(self) -> None:
            self.image_collections: [str] = []
            self.scene_to_process: str = None
            self.scene_to_complete: str = None
            self.preset: str = None

    class Outputs:
        def __init__(self) -> None:
            self.scene: str = None

    class Options:
        def __init__(self) -> None:
            self.recursive_image_collections: bool = None
            self.altitude_reference: AltitudeReference = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[FillImagePropertiesSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=FillImagePropertiesSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=FillImagePropertiesSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = FillImagePropertiesSpecifications()

        try:
            if "imageCollections" in specifications_json["inputs"]:
                collections = []
                for collection in specifications_json["inputs"]["imageCollections"]:
                    collections.append(collection)
                specifications.inputs.image_collections = collections
            if "sceneToProcess" in specifications_json["inputs"]:
                specifications.inputs.scene_to_process = specifications_json["inputs"]["sceneToProcess"]
            if "sceneToComplete" in specifications_json["inputs"]:
                specifications.inputs.scene_to_complete = specifications_json["inputs"]["sceneToComplete"]
            if "preset" in specifications_json["inputs"]:
                specifications.inputs.preset = specifications_json["inputs"]["preset"]

            if "scene" in specifications_json["outputs"]:
                specifications.outputs.scene = specifications_json["outputs"]["scene"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")