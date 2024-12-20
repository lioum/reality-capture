# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from reality_apis.utils import RealityDataType
from reality_apis.DataTransfer.references import ReferenceTable
from utils import authenticate_with_spa_client

def main():
    # This example shows how to upload a context scene (that references local images) in Reality Management.
    # For more information about Reality Management, see : https://developer.bentley.com/apis/reality-management/overview/

    # Inputs
    itwin_id = "your iTwin id."
    client_id = "your iTwin client id"
    context_scene = r"path to the context scene you cant to upload in Reality Management"
    context_scene_name = "name of the context scene"
    images = r"path to the images referenced in the context scene"
    images_name = "name of the dataset"

    print("Authentication...")
    service_manager = authenticate_with_spa_client(client_id)
    print("Authentication done!")

    # First of all, you must upload all the data referenced in the context scene.
    # Then, you must patch the context scene to replace local paths with reality data ids, otherwise the uploaded context scene will reference local data.
    # To make this step easier, we are going to use a reference table. This reference table associates a local path with a reality data id.
    # When the context scene is uploaded, the local paths are replaced with reality data id, so it can be used in the analysis jobs
    references = ReferenceTable()

    # First, upload the images
    print("Start uploading images...")
    ret_up_images = service_manager.management.upload_reality_data(
        images,
        images_name,
        RealityDataType.CCImageCollection, # Type of data, see https://developer.bentley.com/apis/reality-management/rm-rd-details/
        itwin_id,
    )
    if ret_up_images.is_error():
        print("Error in upload :", ret_up_images.error)
        return
    print("Successfully uploaded images")
    print("This your images reality data id :", ret_up_images.value) # Guid Identifier of the reality data
    references.add_reference(images, ret_up_images.value) # Add the images path and the reality data id in the reference table

    # Then, upload the context scene
    print("Start uploading context scene...")
    ret_up_cs = service_manager.management.upload_context_scene(context_scene, context_scene_name, itwin_id, references)
    if ret_up_cs.is_error():
        print("Error in upload:", ret_up_cs.error)
        return
    print("Successfully uploaded context scene")
    print("This your context scene reality data id :", ret_up_cs.value)  # Guid Identifier of the reality data

if __name__ == "__main__":
    main()
