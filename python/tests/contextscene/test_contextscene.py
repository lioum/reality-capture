import json
from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pydantic
import pytest
from contextscene.contextscene import ContextSceneModel, FilePath, resolve_file_path


@pytest.fixture
def basic_cs():
    loaded = Path(
        "python/tests/contextscene/artifacts/photoCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)
    return cs


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


def test_validation_should_fail_on_bad_assignation_reference():
    loaded = Path(
        "python/tests/contextscene/artifacts/photoCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)
    with pytest.raises(pydantic.ValidationError):
        reference = cs.references
        reference["33"] = "my_path"
        cs.references = reference


def test_validation_should_fail_on_bad_key_reference():
    loaded = Path(
        "python/tests/contextscene/artifacts/photoCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)
    with pytest.raises(ValueError):
        reference = cs.references
        reference["3.2"] = {"path": "test_path"}
        cs.references = reference


# def test_add_item_with_object():
#     loaded = Path(
#         "python/tests/contextscene/artifacts/photoCollection_basic.json"
#     ).read_text()
#     cs = ContextSceneModel.model_validate_json(loaded)
#     ref_id = cs.add_or_get_reference("test_path")
#     cs.photo_collection.add_photo(ContextSceneModel.PhotoCollectionModel.PhotoModel(image_path=f"{ref_id}:my_path.png"))


def test_add_or_get_reference(basic_cs):
    ref_id = basic_cs.add_or_get_reference("test_path")
    ref_id2 = basic_cs.add_or_get_reference("test_path")
    assert ref_id == ref_id2


def test_add_item_with_dict():
    loaded = Path(
        "python/tests/contextscene/artifacts/meshCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)
    ref_id = cs.add_or_get_spatial_reference("test_definition")
    ref_id2 = cs.add_or_get_spatial_reference("test_definition")
    assert ref_id == ref_id2
    cs.mesh_collection.srs_id = ref_id


def test_serialize():
    loaded = Path(
        "python/tests/contextscene/artifacts/meshCollection_basic.json"
    ).read_text()
    cs = ContextSceneModel.model_validate_json(loaded)

    with pytest.raises(pydantic.ValidationError):
        cs.references[99] = "23"  # mutable change to a dictionnary
        cs.serialize()


def test_resolve_file_path(basic_cs):
    file = basic_cs.photo_collection.photos["0"].image_path
    ref, name = file.split(":")
    assert (
        resolve_file_path(FilePath(ref, name), basic_cs.references)
        == basic_cs.references[str(ref)].path + name
    )
    assert (
        resolve_file_path(file, basic_cs.references)
        == basic_cs.references[str(ref)].path + name
    )
