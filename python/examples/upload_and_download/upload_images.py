# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from reality_apis.utils import RealityDataType
from utils import authenticate_with_spa_client

def main():
    # This example shows how to upload images in Reality Management.
    # For more information about Reality Management, see : https://developer.bentley.com/apis/reality-management/overview/

    # Inputs
    itwin_id = "your iTwin id."
    client_id = "your iTwin client id"
    images = r"path to the images folder you want to upload in Reality Management"
    images_name = "name of the dataset"

    print("Authentication...")
    service_manager = authenticate_with_spa_client(client_id)
    print("Authentication done!")

    print("Start uploading images...")
    ret_up = service_manager.management.upload_reality_data(
        images,
        images_name,
        RealityDataType.CCImageCollection, # Type of data, see https://developer.bentley.com/apis/reality-management/rm-rd-details/
        itwin_id,
    )
    if ret_up.is_error():
        print("Error in upload :", ret_up.error)
        return
    print("Successfully uploaded images")
    print("This your images reality data id :", ret_up.value) # Guid Identifier of the reality data

if __name__ == "__main__":
    main()
