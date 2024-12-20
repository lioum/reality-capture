# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os

from utils import authenticate_with_spa_client

def main():
    # This example shows how to download data, for instance images, from Reality Management.
    # For more information about Reality Management, see : https://developer.bentley.com/apis/reality-management/overview/

    # Inputs
    itwin_id = "your iTwin id"
    client_id = "your client id"
    reality_data_id = r"your reality data id" # Guid Identifier of the reality data
    output_path = r"path to the folder where you want to download the data"

    print("Authentication...")
    service_manager = authenticate_with_spa_client(client_id)
    print("Authentication done!")

    print("Start uploading images...")
    images_path = os.path.join(output_path, "images")
    ret_down = service_manager.management.download_reality_data(reality_data_id, images_path, itwin_id)
    if ret_down.is_error():
        print("Error while downloading reality_data {}: {}".format(reality_data_id, ret_down.error))

    print("Successfully donwloaded images locally")

if __name__ == "__main__":
    main()
