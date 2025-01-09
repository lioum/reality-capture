# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from __future__ import annotations
from typing import NamedTuple, List
from enum import Enum

from reality_apis.utils import ReturnValue

import json
import os

class RigSynchro(Enum):
    NoRigSynchro = 0
    Strict = 1
    Loose = 2

class RotationPolicy(Enum):
    Compute = 0
    Adjust = 1
    Keep = 2

class CenterPolicy(Enum):
    Compute = 0
    Adjust = 1
    AdjustWithinTolerance = 2
    Keep = 3

class FocalPolicy(Enum):
    Adjust = 0
    Keep = 1

class PrincipalPolicy(Enum):
    Adjust = 0
    Keep = 1

class RadialPolicy(Enum):
    Adjust = 0
    Keep = 1

class TangentialPolicy(Enum):
    Adjust = 0
    Keep = 1

class FisheyeFocalPolicy(Enum):
    AdjustSymmetric = 0
    AdjustAsymmetric = 1
    Keep = 2

class FisheyeDistortionPolicy(Enum):
    Adjust_01xx0 = 0
    Adjust_x1xx0 = 1
    Adjust_x1xxx = 2
    Keep = 3

class AspectRatioPolicy(Enum):
    Adjust = 0
    Keep = 1

class SkewPolicy(Enum):
    Adjust = 0
    Keep = 1

class TiepointsPolicy(Enum):
    Adjust = 0
    Keep = 1

class PairSelection(Enum):
    Default = 0
    Sequence = 1
    Loop = 2
    Exhaustive = 3
    SimilarOnly = 4

class KeypointsDensity(Enum):
    Normal = 0
    High = 1

class TiepointsPolicy(Enum):
    Normal = 0
    High = 1

class Tag(Enum):
    QR = 0
    April = 1
    Chili = 2

class ColorEqualization(Enum):
    NoEqualization = 0
    BlockWise = 1
    MachineLearning = 2

class AdjustmentConstraints(Enum):
    NoAdjustment = 0
    ControlPoints = 1
    PositionMetadata = 2
    PointClouds = 3
    Automatic = 4

class RigidRegistrationPosition(Enum):
    NoPosition = 0
    UserConstraints = 1
    ControlPoints = 2
    PositionMetadata = 3
    PointClouds = 4
    Automatic = 5

class RigidRegistrationRotation(Enum):
    NoRotation = 0
    UserConstraints = 1
    ControlPoints = 2
    PositionMetadata = 3
    PointClouds = 4
    Automatic = 5
    RotationMetadata = 6

class RigidRegistrationScale(Enum):
    NoScale = 0
    UserConstraints = 1
    ControlPoints = 2
    PositionMetadata = 3
    PointClouds = 4
    Automatic = 5

class CalibrationSpecifications:
    def __init__(self) -> None:
        self.inputs = self.Inputs()
        self.outputs = self.Outputs()
        self.options = self.Options()

    def get_type(self) -> str:
        return "Calibration"

    class Inputs:
        def __init__(self) -> None:
            self.scene: str = ""
            self.preset: str = None

    class Outputs:
        def __init__(self) -> None:
            self.context_scene: str = None
            self.orientations: str = None
            self.report: str = None
            self.splats: str = None

    class Options:
        def __init__(self) -> None:
            self.rig_synchro: RigSynchro = None
            self.rotation_policy: RotationPolicy = None
            self.center_policy: CenterPolicy = None
            self.center_tolerance: float = None
            self.focal_policy: FocalPolicy = None
            self.principal_policy: PrincipalPolicy = None
            self.radial_policy: RadialPolicy = None
            self.tangential_policy: TangentialPolicy = None
            self.fisheye_focal_policy: FisheyeFocalPolicy = None
            self.fisheye_distortion_policy: FisheyeDistortionPolicy = None
            self.aspect_ratio_policy: AspectRatioPolicy = None
            self.skew_policy: SkewPolicy = None
            self.tiepoints_policy: TiepointsPolicy = None
            self.pair_selection: PairSelection = None
            self.pair_selection_distance: int = None
            self.keypoints_density: KeypointsDensity = None
            self.precalibration: bool = None
            self.tags_extraction: list[Tag] = None
            self.color_equalization: ColorEqualization = None
            self.adjustment_constraints: list[AdjustmentConstraints] = None
            self.rigid_registration_position: RigidRegistrationPosition = None
            self.rigid_registration_rotation: RigidRegistrationRotation = None
            self.rigid_registration_scale: RigidRegistrationScale = None
            self.workspace: str = None

    @classmethod
    def from_json_file(cls, json_file: str) -> ReturnValue[CalibrationSpecifications]:
        if not os.path.isfile(json_file):
            return ReturnValue(value=CalibrationSpecifications(), error="File not found: " + json_file)
        try:
            with open(json_file, encoding='utf-8') as f:
                specifications_json = json.load(f)
        except Exception as e:
            return ReturnValue(value=CalibrationSpecifications(),
                               error=f"Failed to load specifications {json_file}: {e}")

        specifications = CalibrationSpecifications()

        try:
            if "scene" in specifications_json["inputs"]:
                specifications.inputs.scene = specifications_json["inputs"]["scene"]

            if "contextScene" in specifications_json["outputs"]:
                specifications.outputs.context_scene = specifications_json["outputs"]["contextScene"]
            if "orientations" in specifications_json["outputs"]:
                specifications.outputs.orientations = specifications_json["outputs"]["orientations"]
            if "report" in specifications_json["outputs"]:
                specifications.outputs.report = specifications_json["outputs"]["report"]
            if "splats" in specifications_json["outputs"]:
                specifications.outputs.splats = specifications_json["outputs"]["splats"]

            if "options" in specifications_json:
                if "rigSynchro" in specifications_json["options"]:
                    specifications.options.rig_synchro = RigSynchro[specifications_json["options"]["rigSynchro"]]
                if "rotationPolicy" in specifications_json["options"]:
                    specifications.options.rotation_policy = RotationPolicy[specifications_json["options"]["rotationPolicy"]]
                if "centerPolicy" in specifications_json["options"]:
                    specifications.options.center_policy = CenterPolicy[specifications_json["options"]["centerPolicy"]]
                if "centerTolerance" in specifications_json["options"]:
                    specifications.options.center_tolerance = specifications_json["options"]["centerTolerance"]
                if "focalPolicy" in specifications_json["options"]:
                    specifications.options.focal_policy = FocalPolicy[specifications_json["options"]["focalPolicy"]]
                if "principalPolicy" in specifications_json["options"]:
                    specifications.options.principal_policy = PrincipalPolicy[specifications_json["options"]["principalPolicy"]]
                if "radialPolicy" in specifications_json["options"]:
                    specifications.options.radial_policy = RadialPolicy[specifications_json["options"]["radialPolicy"]]
                if "tangentialPolicy" in specifications_json["options"]:
                    specifications.options.tangential_policy = TangentialPolicy[specifications_json["options"]["tangentialPolicy"]]
                if "fisheyeFocalPolicy" in specifications_json["options"]:
                    specifications.options.fisheye_focal_policy = FisheyeFocalPolicy[specifications_json["options"]["fisheyeFocalPolicy"]]
                if "fisheyeDistortionPolicy" in specifications_json["options"]:
                    specifications.options.fisheye_distortion_policy = FisheyeDistortionPolicy[specifications_json["options"]["fisheyeDistortionPolicy"]]
                if "aspectRatioPolicy" in specifications_json["options"]:
                    specifications.options.aspect_ratio_policy = AspectRatioPolicy[specifications_json["options"]["aspectRatioPolicy"]]
                if "skewPolicy" in specifications_json["options"]:
                    specifications.options.skew_policy = SkewPolicy[specifications_json["options"]["skewPolicy"]]
                if "tiepointsPolicy" in specifications_json["options"]:
                    specifications.options.tiepoints_policy = TiepointsPolicy[specifications_json["options"]["tiepointsPolicy"]]
                if "pairSelection" in specifications_json["options"]:
                    specifications.options.pair_selection = PairSelection[specifications_json["options"]["pairSelection"]]
                if "pairSelectionDistance" in specifications_json["options"]:
                    specifications.options.pair_selection_distance = specifications_json["options"]["pairSelectionDistance"]
                if "keypointsDensity" in specifications_json["options"]:
                    specifications.options.keypoints_density = KeypointsDensity[specifications_json["options"]["keypointsDensity"]]
                if "precalibration" in specifications_json["options"]:
                    specifications.options.precalibration = specifications_json["options"]["precalibration"]
                if "tagsExtraction" in specifications_json["options"]:
                    tag_list = []
                    for tag in specifications_json["options"]["tagsExtraction"]:
                        tag_list.append(Tag[tag])
                    specifications.options.tags_extraction = tag_list
                if "colorEqualization" in specifications_json["options"]:
                    specifications.options.color_equalization = ColorEqualization[specifications_json["options"]["colorEqualization"]]
                if "adjustmentConstraints" in specifications_json["options"]:
                    adjustment_list = []
                    for adjustment in specifications_json["options"]["adjustmentConstraints"]:
                        adjustment_list.append(AdjustmentConstraints[adjustment])
                    specifications.options.adjustment_constraints = adjustment_list
                if "rigidRegistrationPosition" in specifications_json["options"]:
                    specifications.options.rigid_registration_position = RigidRegistrationPosition[specifications_json["options"]["rigidRegistrationPosition"]]
                if "rigidRegistrationRotation" in specifications_json["options"]:
                    specifications.options.rigid_registration_rotation = RigidRegistrationRotation[specifications_json["options"]["rigidRegistrationRotation"]]
                if "rigidRegistrationScale" in specifications_json["options"]:
                    specifications.options.rigid_registration_scale = RigidRegistrationScale[specifications_json["options"]["rigidRegistrationScale"]]
                if "workspace" in specifications_json["options"]:
                    specifications.options.workspace = specifications_json["options"]["workspace"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")