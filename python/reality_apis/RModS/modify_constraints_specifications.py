# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations

from reality_apis.utils import ReturnValue

import json
import os
from enum import Enum

class ConstraintType(Enum):
    Mesh = 0
    Polygon = 1

class ConstraintToAdd:
    def __init__(self) -> None:
        self.constraint_path: str = ""
        self.srs: str = ""
        self.type: ConstraintType = None
        self.resolution: float = None
        self.texture_path: str = None
        self.texture_size: int = None
        self.fill_color: str = None
        self.name: str = None
        self.description: str = None

class ModifyConstraintsSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()

    def get_type(self) -> str:
        return "Constraints"

    class Inputs:
        def __init__(self) -> None:
            self.reference_model: str = ""
            self.constraints_to_delete: list[str] = None
            self.constraints_to_add: list[ConstraintToAdd] = None

    class Outputs:
        def __init__(self) -> None:
            self.added_constraints_info: str = ""

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[ModifyConstraintsSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=ModifyConstraintsSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=ModifyConstraintsSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = ModifyConstraintsSpecifications()

        try:
            specifications.inputs.reference_model = specifications_json["inputs"]["referenceModel"]
            if "constraintsToDelete" in specifications_json["inputs"]:
                constraints_to_delete = []
                for constraint_to_delete in specifications_json["inputs"]["constraintsToDelete"]:
                    constraints_to_delete.append(constraint_to_delete)
                specifications.inputs.constraints_to_delete = constraints_to_delete
            if "constraintsToAdd" in specifications_json["inputs"]:
                constraints_to_add = []
                for constraint_json in specifications_json["inputs"]["constraintsToAdd"]:
                    constraint = ConstraintToAdd()
                    constraint.constraint_path = constraint_json["constraintPath"]
                    constraint.srs = constraint_json["srs"]
                    if "type" in constraint_json:
                        if constraint_json["type"] == "Mesh":
                            constraint.type = ConstraintType.Mesh
                        if constraint_json["type"] == "Polygon":
                            constraint.type = ConstraintType.Polygon
                    if "resolution" in constraint_json:
                        constraint.resolution = constraint_json["resolution"]
                    if "texturePath" in constraint_json:
                        constraint.texture_path = constraint_json["texturePath"]
                    if "textureSize" in constraint_json:
                        constraint.texture_size = constraint_json["textureSize"]
                    if "fillColor" in constraint_json:
                        constraint.fill_color = constraint_json["fillColor"]
                    if "name" in constraint_json:
                        constraint.name = constraint_json["name"]
                    if "description" in constraint_json:
                        constraint.description = constraint_json["description"]
                    constraints_to_add.append(constraint)
                specifications.inputs.constraints_to_add = constraints_to_add

            specifications.outputs.added_constraints_info = specifications_json["outputs"]["addedConstraintsInfo"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")