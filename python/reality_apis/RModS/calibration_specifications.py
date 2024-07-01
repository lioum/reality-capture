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
            self.photos: str = None
            self.point_clouds: str = None
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
            if "Photos" in specifications_json["Inputs"]:
                specifications.inputs.photos = specifications_json["Inputs"]["Photos"]
            if "Pointclouds" in specifications_json["Inputs"]:
                specifications.inputs.point_clouds = specifications_json["Inputs"]["Pointclouds"]

            if "ContextScene" in specifications_json["Outputs"]:
                specifications.outputs.context_scene = specifications_json["Outputs"]["ContextScene"]
            if "Orientations" in specifications_json["Outputs"]:
                specifications.outputs.orientations = specifications_json["Outputs"]["Orientations"]

        except Exception as e:
            return ReturnValue(value=specifications, error=str(e))
        return ReturnValue(value=specifications, error="")