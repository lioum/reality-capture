# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

NUM_DECIMALS = 50  # Round the bbox location to 'x' decimals as a percentage of the entire image len and width.
# Note this is also used for the number of decimals for the confidence in the prediction.


class ConstextSceneMissingDevice(Exception):
    pass


class ConstextSceneMultipleTaskNotSupported(Exception):
    pass


class InvalidPathFormat(Exception):
    pass


def to_camel_specific(string: str) -> str:
    """
    Convert from python snake_case to json Upper camel case convention.
    This function is overwrited by the 'alias' argument of the BaseModel.Field class.
    """
    special_conversion = {"2d": "2D", "3d": "3D"}
    words = string.split("_")
    capitalized_words = []
    for word in words:
        modified_word = word.capitalize()
        if word in special_conversion.keys():
            modified_word = special_conversion[word]
        capitalized_words.append(modified_word)
    return "".join(capitalized_words)


class FilePath:
    def __init__(self, path: str) -> None:
        self._str_path = path
        self._reference_id, self._relative_path = self.parse_path_with_ref(
            self._str_path
        )

    def __str__(self) -> str:
        if self.reference_id is not None:
            return f"{self._reference_id}:{str(self._relative_path)}"

    @staticmethod
    def parse_path_with_ref(path_str: str):
        splits = path_str.split(":")
        if len(splits) != 2:
            raise InvalidPathFormat(
                f"The path '{path_str}' is invalid. File path in a context scene must be of this format: <ref_id>:<file_path> ."
            )
        else:
            return (splits[0], splits[1])

    @property
    def reference_id(self):
        return self._reference_id

    @property
    def relative_path(self):
        return self._relative_path


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel_specific,
        populate_by_name=True,
        extra="forbid",
        validate_assignment=True,
    )  # Forbid, ingore or allow? Allow would enable people to store custom information, but without validation


class ContextSceneModel(BaseConfigModel):
    class RefPathModel(BaseConfigModel):
        path: str

        @field_validator("path")
        @classmethod
        def check_format(cls, v):
            FilePath(v)

    class SpatialReferenceSystemModel(BaseConfigModel):
        definition: str

    class PhotoCollectionModel(BaseConfigModel):
        class DevicesModel(BaseConfigModel):
            class DimensionsModel(BaseConfigModel):
                width: int = Field(alias="width")
                height: int = Field(alias="height")

            class PrincipalPointModel(BaseConfigModel):
                x: float = Field(alias="x")
                y: float = Field(alias="y")

            class RadialDistortionModel(BaseConfigModel):
                k1: float = Field(alias="k1")
                k2: float = Field(alias="k2")
                k3: float = Field(alias="k3")

            class TangentialDistortionModel(BaseConfigModel):
                p1: float = Field(alias="p1")
                p2: float = Field(alias="p2")

            class PixelSizeModel(BaseConfigModel):
                width: float  # TODO: Check actual naming convention Upper vs Lower, compare to DimensionModel
                height: float

            type: str  # TODO: Add choice here
            dimensions: DimensionsModel
            principal_point: Optional[PrincipalPointModel] = None
            focal_length: Optional[float] = None
            radial_distortion: Optional[RadialDistortionModel] = None
            tangential_distortion: Optional[TangentialDistortionModel] = None
            aspect_ratio: Optional[float] = None
            skew: Optional[float] = None
            pixel_size: Optional[PixelSizeModel] = None
            no_data: int = None

        class PosesModel(BaseConfigModel):
            class CenterModel(BaseConfigModel):  # Duplicated model
                x: float = Field(alias="x")
                y: float = Field(alias="y")
                z: float = Field(alias="z")

            class RotationModel(BaseConfigModel):
                omega: float = Field(alias="omega")
                phi: float = Field(alias="phi")
                kappa: float = Field(alias="kappa")

            center: CenterModel
            rotation: RotationModel = None

        class PhotosModel(BaseConfigModel):
            class LocationModel(BaseConfigModel):
                ul_x: float
                ul_y: float

            image_path: str
            device_id: Optional[int] = None
            pose_id: Optional[int] = None
            location: Optional[LocationModel] = None
            depth_path: Optional[str] = None

            @field_validator("depth_path", "image_path")
            @classmethod
            def check_format(cls, v):
                FilePath(v)

        srs_id: int = Field(None, alias="SRSId")
        photos: Dict[str, PhotosModel]
        devices: Optional[Dict[str, DevicesModel]] = None
        poses: Optional[Dict[str, PosesModel]] = None

        # TODO: have validators to test referenced ids against reference dict.
        @field_validator("devices")
        def check_devices(cls, v, values):
            """
            We want to make sure that referenced ids exists in the contextScene.
            """
            pass

    class MeshCollectionModel(BaseConfigModel):
        class MeshModel(BaseConfigModel):
            class Box3DModel(BaseConfigModel):  # TODO: duplicated model
                xmin: float = Field(alias="xmin")
                ymin: float = Field(alias="ymin")
                zmin: float = Field(alias="zmin")
                xmax: float = Field(alias="xmax")
                ymax: float = Field(alias="ymax")
                zmax: float = Field(alias="zmax")

            name: str = ""
            path: str
            bounding_box: Box3DModel = None

            @field_validator("path")
            @classmethod
            def check_format(cls, v):
                FilePath(v)

        srs_id: int = Field(None, alias="SRSId")
        meshes: Dict[str, MeshModel]

    class PointCloudCollection(BaseConfigModel):
        class PointCloudModel(BaseConfigModel):
            class CenterModel(BaseConfigModel):  # Duplicated model
                x: float = Field(alias="x")
                y: float = Field(alias="y")
                z: float = Field(alias="z")

            class Box3DModel(BaseConfigModel):  # TODO: duplicated model
                xmin: float = Field(alias="xmin")
                ymin: float = Field(alias="ymin")
                zmin: float = Field(alias="zmin")
                xmax: float = Field(alias="xmax")
                ymax: float = Field(alias="ymax")
                zmax: float = Field(alias="zmax")

            name: str = ""
            bounding_box: Box3DModel = None
            path: str
            type: str = None  # Possible value ("Mobile", "Static")
            location: str = None  # Possible value ("InFile","Unknown")
            center: CenterModel = None
            trajectory_id: int = None
            srs_id: int = Field(
                None, alias="SRSId"
            )  # TODO Present in one example. Check if correct

            @field_validator("path")
            @classmethod
            def check_format(cls, v):
                FilePath(v)

            # TODO: Multiple validation to do depending of the type of file, or the value of location

        srs_id: int = Field(
            None, alias="SRSId"
        )  # TODO valid if present for certain type of files
        point_clouds: Dict[str, PointCloudModel]

    class TrajectoryCollection(BaseConfigModel):
        class TrajectoryModel(BaseConfigModel):
            paths: List[str] = Field(min_length=1)
            delimiters: List[str]  # =[" ", ","] # TODO: check if valid default value
            combine_consecutive_delimiters: bool  # = True
            decimal_separator: str  # = "."
            lines_to_ignore: int
            time_column_id: int
            x_column_id: int
            y_column_id: int
            z_column_id: int

        trajectories: dict[str, TrajectoryModel]
        srs_id: int = Field(None, alias="SRSId")

    class AnnotationsModel(BaseConfigModel):
        class LabelsModel(BaseConfigModel):
            name: str

        class Object2DModel(BaseConfigModel):
            class LabelInfoModel(BaseConfigModel):
                label_id: int  # Note LabelId is an int here as a value, but is a str as a key under Annotations.Labels
                confidence: Optional[
                    float
                ] = None  # This identifies original annotations, not predictions.

            class Box2DModel(BaseConfigModel):
                xmin: float = Field(alias="xmin")
                xmax: float = Field(alias="xmax")
                ymin: float = Field(alias="ymin")
                ymax: float = Field(alias="ymax")

            class TextInfoModel(BaseConfigModel):
                text: str
                orientation: int

            label_info: LabelInfoModel
            box_2d: Box2DModel
            text_info: TextInfoModel = None

        class objects3DModel(BaseConfigModel):
            class Object3DModel(BaseConfigModel):
                class LabelInfoModel(BaseConfigModel):
                    label_id: int

                class RotatedBox3DModel(BaseConfigModel):
                    class Box3DModel(BaseConfigModel):
                        xmin: float = Field(alias="xmin")
                        ymin: float = Field(alias="ymin")
                        zmin: float = Field(alias="zmin")
                        xmax: float = Field(alias="xmax")
                        ymax: float = Field(alias="ymax")
                        zmax: float = Field(alias="zmax")

                    class RotationModel(BaseConfigModel):
                        M_00: float = Field(alias="M_00")
                        M_01: float = Field(alias="M_01")
                        M_02: float = Field(alias="M_02")
                        M_10: float = Field(alias="M_10")
                        M_11: float = Field(alias="M_11")
                        M_12: float = Field(alias="M_12")
                        M_20: float = Field(alias="M_20")
                        M_21: float = Field(alias="M_21")
                        M_22: float = Field(alias="M_22")

                    box_3d: Box3DModel
                    rotation: RotationModel

                class TextInfoModel(BaseConfigModel):
                    text: str
                    orientation: int

                label_info: LabelInfoModel
                rotated_box_3d: RotatedBox3DModel

            objects: dict[str, Object3DModel]
            srs_id: int = Field(None, alias="SRSId")  # TODO optional or not

        class Segmentation2DModel(BaseConfigModel):
            path: str

            @field_validator("path")
            @classmethod
            def check_format(cls, v):
                FilePath(v)

        class Segmentation3DModel(BaseConfigModel):
            srs_id: int = Field(None, alias="SRSId")
            path: str

            @field_validator("path")
            @classmethod
            def check_format(cls, v):
                FilePath(v)

        class Polygons2DModel(BaseConfigModel):
            class Polygon2DModel(BaseConfigModel):
                class LabelInfoModel(BaseConfigModel):
                    label_id: int

                class VerticeModel(BaseConfigModel):
                    class PositionModel(BaseConfigModel):
                        x: float = Field(alias="x")
                        y: float = Field(alias="y")

                    position: PositionModel

                class BoundaryModel(BaseConfigModel):
                    vertex_ids: List[int]

                label_info: LabelInfoModel
                area: float
                vertices: Dict[str, VerticeModel]
                outer_boundary: BoundaryModel
                inner_boundaries: List[BoundaryModel] = None

            srs_id: int = Field(None, alias="SRSId")
            polygons: Optional[Dict[str, Polygon2DModel]]

        class Lines2DModel(BaseConfigModel):
            class Line2DModel(BaseConfigModel):
                class LabelInfoModel(BaseConfigModel):
                    label_id: int

                class VerticeModel(BaseConfigModel):
                    class PositionModel(BaseConfigModel):
                        x: float = Field(alias="x")
                        y: float = Field(alias="y")

                    position: PositionModel
                    diameter: float

                class VertexModel(BaseConfigModel):
                    vertex_id_1: int
                    vertex_id_2: int

                label_info: LabelInfoModel
                length: float
                mean_diameter: float
                max_diameter: float
                vertices: Dict[str, VerticeModel]
                segments: List[VertexModel]

            srs_id: int = Field(None, alias="SRSId")
            lines: Dict[str, Line2DModel]

        class Lines3DModel(BaseConfigModel):
            class Line3DModel(BaseConfigModel):
                class LabelInfoModel(BaseConfigModel):
                    label_id: int

                class VerticeModel(BaseConfigModel):
                    class PositionModel(BaseConfigModel):
                        x: float = Field(alias="x")
                        y: float = Field(alias="y")
                        z: float = Field(alias="z")

                    position: PositionModel
                    diameter: float

                class VertexModel(BaseConfigModel):
                    vertex_id_1: int
                    vertex_id_2: int

                label_info: LabelInfoModel
                length: float
                mean_diameter: float
                max_diameter: float
                vertices: Dict[str, VerticeModel]
                segments: List[VertexModel]

            srs_id: int = Field(None, alias="SRSId")
            lines: Dict[str, Line3DModel]

        labels: Dict[str, LabelsModel]
        objects_2d: Optional[Dict[str, Dict[str, Object2DModel]]] = None
        objects_3d: Optional[objects3DModel] = None
        segmentation_2d: Optional[Dict[str, Segmentation2DModel]] = None
        segmentation_3d: Optional[Segmentation3DModel] = None
        polygons_2d: Optional[Polygons2DModel] = None
        lines_2d: Optional[Lines2DModel] = None
        lines_3d: Optional[Lines3DModel] = None

    version: str = Field("5.0", strict=True, alias="version")
    spatial_reference_systems: Optional[Dict[str, SpatialReferenceSystemModel]] = None
    photo_collection: Optional[PhotoCollectionModel] = None
    mesh_collection: Optional[MeshCollectionModel] = None
    point_cloud_collection: Optional[PointCloudCollection] = None
    trajectory_collection: Optional[TrajectoryCollection] = None
    annotations: Optional[AnnotationsModel] = None
    references: Optional[Dict[str, RefPathModel]] = None

    def serialize(self):
        return self.model_dump_json(by_alias=True, exclude_none=True)

    def serialize_schema(self):
        return self.model_json_schema(by_alias=True)

    def unserialize(self, s: str):
        return self.model_validate_json(s)
