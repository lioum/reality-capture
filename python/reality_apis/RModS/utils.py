# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from reality_apis.RModS.reconstruction_specifications import ReconstructionSpecifications
from reality_apis.RModS.calibration_specifications import CalibrationSpecifications

from typing import TypeVar

Specifications = TypeVar(
    "Specifications",
    ReconstructionSpecifications,
    CalibrationSpecifications
)