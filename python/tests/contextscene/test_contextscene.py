import json
from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pydantic
import pytest
from python.contextscene.contextscene_pydantic import ContextSceneModel


def test_schema_serialization():
    Path("python/contextscene/schema.json").write_text(
        json.dumps(ContextSceneModel.model_json_schema(by_alias=True), indent=4)
    )


@pytest.mark.parametrize(
    "artifact_path",
    [
        ("python/tests/contextscene/artifacts/photoCollection_basic.json"),
        (
            "python/tests/contextscene/artifacts/photoCollection_orthophoto_with_height.json"
        ),
        ("python/tests/contextscene/artifacts/photoCollection_orthophoto.json"),
        ("python/tests/contextscene/artifacts/photoCollection_with_orientations.json"),
        ("python/tests/contextscene/artifacts/photoCollection_with_positions.json"),
    ],
)
def test_photo_collection_valid(artifact_path):
    loaded = Path(artifact_path).read_text()
    ContextSceneModel.model_validate_json(loaded)


@pytest.mark.parametrize(
    "artifact_path",
    [
        ("python/tests/contextscene/artifacts/annotations_lines2D.json"),
        ("python/tests/contextscene/artifacts/annotations_lines3D.json"),
        ("python/tests/contextscene/artifacts/annotations_objects3D.json"),
        ("python/tests/contextscene/artifacts/annotations_objects2D.json"),
        ("python/tests/contextscene/artifacts/annotations_polygons2D.json"),
        ("python/tests/contextscene/artifacts/annotations_segmentation2D.json"),
        ("python/tests/contextscene/artifacts/annotations_segmentation3D.json"),
    ],
)
def test_annotation_valid(artifact_path):
    loaded = Path(artifact_path).read_text()
    ContextSceneModel.model_validate_json(loaded)


@pytest.mark.parametrize(
    "artifact_path",
    [
        ("python/tests/contextscene/artifacts/PointCloudCollection_pod.json"),
        ("python/tests/contextscene/artifacts/PointCloudCollection_opc.json"),
        ("python/tests/contextscene/artifacts/PointCloudCollection_las.json"),
        (
            "python/tests/contextscene/artifacts/PointCloudCollection_las_with_unknown_location.json"
        ),
        (
            "python/tests/contextscene/artifacts/PointCloudCollection_las_with_location.json"
        ),
        ("python/tests/contextscene/artifacts/PointCloudCollection_e57.json"),
        ("python/tests/contextscene/artifacts/PointCloudCollection_e57.json"),
    ],
)
def test_point_cloud_valid(artifact_path):
    loaded = Path(artifact_path).read_text()
    ContextSceneModel.model_validate_json(loaded)


@pytest.mark.parametrize(
    "artifact_path",
    [("python/tests/contextscene/artifacts/TrajectoryCollection.json")],
)
def test_trajectory_collection_valid(artifact_path):
    loaded = Path(artifact_path).read_text()
    ContextSceneModel.model_validate_json(loaded)


def test_validation_should_fail_on_bad_assignation():
    loaded = Path(
        "python/tests/contextscene/artifacts/photoCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)
    with pytest.raises(pydantic.ValidationError):
        cs.mesh_collection = ""
