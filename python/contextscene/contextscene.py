# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import json
from typing import Dict, List, Optional, Union

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
    """
    Helper class to manipulate a string path of this format <reference_id>:<file_path>
    """

    def __init__(self, reference_id: str, relative_path: str) -> None:
        self._reference_id = reference_id
        self._relative_path = relative_path

    def __str__(self) -> str:
        if self.reference_id is not None:
            return f"{self._reference_id}:{str(self._relative_path)}"

    @classmethod
    def parse_path_str(cls, path_str: str) -> "FilePath":
        splits = path_str.split(":")
        if len(splits) != 2:
            raise InvalidPathFormat(
                f"The path '{path_str}' is invalid. File path in a context scene must be of this format: <ref_id>:<file_path> ."
            )
        else:
            return cls(splits[0], splits[1])

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
        extra="allow", # TODO: Add everything supported by the APIs, then turn this to 'forbid'.
        validate_assignment=True,
    )  # Forbid, ingore or allow? Allow would enable people to store custom information, but without validation


# def _add_dict_item(field_name, function_name):
#     """
#     Decorator to add add_item method
#     """
#     def decorator(cls):
#         def _add_item(self, item_value:any, id_:str) ->str:
#             dict_field = getattr(self, field_name)
#             if dict_field is None:
#                 dict_field = {}
#             dict_field[str(id_)] = item_value
#             return id_

#         setattr(cls, function_name, _add_item)
#         return cls

#     return decorator


class ContextSceneModel(BaseConfigModel):
    class RefPathModel(BaseConfigModel):
        path: str

    class SpatialReferenceSystemModel(BaseConfigModel):
        definition: str
        name: Optional[str] = None

    # @_add_dict_item(field_name='photos', function_name='add_photo')
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

            center: Optional[CenterModel] = None
            rotation: Optional[RotationModel] = None

        class PhotoModel(BaseConfigModel):
            class LocationModel(BaseConfigModel):
                ul_x: float
                ul_y: float

            image_path: str
            device_id: Optional[int] = None
            pose_id: Optional[int] = None
            location: Optional[LocationModel] = None
            depth_path: Optional[str] = None
            near_depth: Optional[float] = None
            median_depth: Optional[float] = None
            far_depth: Optional[float] = None

            @field_validator("depth_path", "image_path")
            @classmethod
            def check_format(cls, v):
                FilePath.parse_path_str(v) if v is not None else None
                return v

        srs_id: int = Field(default=None, alias="SRSId")
        photos: Dict[str, PhotoModel]
        devices: Optional[Dict[str, DevicesModel]] = None
        poses: Optional[Dict[str, PosesModel]] = None

        # TODO: have validators to test referenced ids against reference dict.
        @field_validator("devices")
        def check_devices(cls, v, values):
            """
            We want to make sure that referenced ids exists in the contextScene.
            """
            return v

    # @_add_dict_item(field_name='meshes',function_name='add_mesh')
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
                FilePath.parse_path_str(v) if v is not None else None
                return v

        srs_id: int = Field(None, alias="SRSId")
        meshes: Dict[str, MeshModel]

    # @_add_dict_item(field_name='point_clouds',function_name='add_point_cloud')
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
                FilePath.parse_path_str(v) if v is not None else None
                return v

            # TODO: Multiple validation to do depending of the type of file, or the value of location

        srs_id: int = Field(
            None, alias="SRSId"
        )  # TODO valid if present for certain type of files
        point_clouds: Dict[str, PointCloudModel]

    # @_add_dict_item(field_name='trajectories',function_name='add_trajectorie')
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

    # @_add_dict_item(field_name='segmentations_2d', function_name='add_segmentation_2d')
    # @_add_dict_item(field_name='objeects_2d', function_name='add_object_2d')
    class AnnotationsModel(BaseConfigModel):
        class LabelModel(BaseConfigModel):
            name: str
            object: bool = None

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

        # @_add_dict_item(field_name='objects',function_name='object')
        class objects3DModel(BaseConfigModel):
            class Object3DModel(BaseConfigModel):
                class LabelInfoModel(BaseConfigModel):
                    label_id: int
                    object: bool = None

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
                FilePath.parse_path_str(v) if v is not None else None
                return v

        class Segmentation3DModel(BaseConfigModel):
            srs_id: int = Field(None, alias="SRSId")
            path: str

            @field_validator("path")
            @classmethod
            def check_format(cls, v):
                FilePath.parse_path_str(v) if v is not None else None
                return v

        # @_add_dict_item(field_name='polygons', function_name='add_polygon')
        class Polygons2DModel(BaseConfigModel):
            # @_add_dict_item(field_name='vertices', function_name='add_vertices')
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

        # @_add_dict_item(field_name='lines', function_name='add_line')
        class Lines2DModel(BaseConfigModel):
            # @_add_dict_item(field_name='vertices', function_name='add_vertice')
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

        # @_add_dict_item(field_name='lines', function_name='add_line')
        class Lines3DModel(BaseConfigModel):
            # @_add_dict_item(field_name='vertices', function_name='add_vertice')
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

        labels: Dict[str, LabelModel]
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

    @field_validator("references", "spatial_reference_systems")
    @classmethod
    def check_ids(cls, v, data):
        # Value must be a int string
        if v is not None:
            for k in v.keys():
                try:
                    int(k)
                except ValueError as e:
                    raise ValueError("reference keys must be an interger string.") from e
        return v

    def add_or_get_reference(self, path: str) -> str:
        """
        Add reference if doesn't exist.
        """
        if self.references is None:
            self.references = {}

        reverse_map = dict(
            zip(
                [x.path for x in self.references.values()], list(self.references.keys())
            )
        )
        idx = reverse_map.get(path)
        if idx is None:
            idx = (
                max([int(x) for x in self.references.keys()]) + 1
                if len(self.references) > 0
                else 0
            )
            idx = str(idx)
            self.references.update({idx: self.RefPathModel(path=path)})
        return idx

    def add_or_get_spatial_reference(self, definition: str) -> str:
        """
        Add spatial reference if doesn't exist.
        """
        definition = definition.upper()
        if self.spatial_reference_systems is None:
            self.spatial_reference_systems = {}

        reverse_map = dict(
            zip(
                [x.definition for x in self.spatial_reference_systems.values()],
                list(self.spatial_reference_systems.keys()),
            )
        )
        idx = reverse_map.get(definition)
        if idx is None:
            idx = (
                max([int(x) for x in self.spatial_reference_systems.keys()]) + 1
                if len(self.spatial_reference_systems) > 0
                else 0
            )
            idx = str(idx)
            self.spatial_reference_systems.update(
                {idx: self.SpatialReferenceSystemModel(definition=definition)}
            )
        return idx

    def serialize(self, validate: bool = True) -> str:
        if validate:
            self.model_validate(self.model_dump(exclude_none=True))
        return self.model_dump_json(by_alias=True, exclude_none=True)

    def serialize_schema(self) -> str:
        return json.dumps(self.model_json_schema(by_alias=True))

    @classmethod
    def deserialize(cls, s: str, validate: bool = True) -> "ContextSceneModel":
        return cls.model_validate_json(s)


def resolve_file_path(
    file_path: Union[str, FilePath],
    references: Dict[str, ContextSceneModel.RefPathModel],
):
    if isinstance(file_path, str):
        file_path = FilePath.parse_path_str(file_path)
    return references[file_path.reference_id].path + file_path.relative_path
