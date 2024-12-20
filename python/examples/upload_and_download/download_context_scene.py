# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os

from reality_apis.DataTransfer.references import ReferenceTable
from utils import authenticate_with_spa_client

def main():
    # This example shows how to download a context scene (that references local images) in Reality Management.
    # For more information about Reality Management, see : https://developer.bentley.com/apis/reality-management/overview/

    # Inputs
    itwin_id = "your iTwin id."
    client_id = "your iTwin client id"
    images_reality_data_id = r"your images reality data id"  # Guid Identifier of the reality data
    cs_reality_data_id = r"your context scene reality data id"  # Guid Identifier of the reality data
    output_path = r"path to the folder where you want to download the data"

    print("Authentication...")
    service_manager = authenticate_with_spa_client(client_id)
    print("Authentication done!")

    # The reality data context scene is referencing other reality data, such as images, meshes and point clouds.
    # First of all, you must download all the data referenced in the context scene reality data.
    # Then, you must patch the context scene to replace reality data ids with local paths, otherwise the download context scene will reference cloud data.
    # To make this step easier, we are going to use a reference table. This reference table associates a reality data id with a local path.
    # When the context scene is downloaded, the reality data ids are replaced with local paths, so you get a valid local context scene
    references = ReferenceTable()

    # First, download the images
    print("Start uploading images...")
    images_path = os.path.join(output_path, "images")
    ret_down_images = service_manager.management.download_reality_data(images_reality_data_id, images_path, itwin_id)
    if ret_down_images.is_error():
        print("Error while downloading reality_data {}: {}".format(images_reality_data_id, ret_down_images.error))
        return
    print("Successfully donwloaded images locally")
    references.add_reference(images_path, images_reality_data_id) # Add the images path and the reality data id in the reference table

    # Then, download the context scene
    print("Start downloading context scene...")
    cs_path = os.path.join(output_path, "scene")
    ret_down_cs = service_manager.management.download_context_scene(cs_reality_data_id, cs_path, itwin_id, references)
    if ret_down_cs.is_error():
        print("Error while downloading reality_data {}: {}".format(cs_reality_data_id, ret_down_cs.error))
        return
    print("Successfully downloaded context scene")

if __name__ == "__main__":
    main()
