# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

from utils import authenticate_with_spa_client
import reality_apis.iTwins.itwins as iTwins

def main():
    # This example shows how to create iTwins.
    # For more information about iTwins, see : https://developer.bentley.com/apis/itwins/overview/

    # Inputs
    client_id = "your client id"
    iTwin_display_name = "The name of your iTwin"
    iTwin_data_center_location = "East US"  # The data center where the data for this iTwin will be persisted

    print("Authentication...")
    service_manager = authenticate_with_spa_client(client_id)
    print("Authentication done!")

    iTwins_settings = iTwins.iTwinSettings()
    iTwins_settings.iTwin_class = iTwins.iTwinClass.ENDEAVOR
    iTwins_settings.iTwin_subclass = iTwins.iTwinSubClass.PROJECT
    iTwins_settings.display_name = iTwin_display_name
    iTwins_settings.data_center_location = iTwin_data_center_location

    print("Creating iTwin...")
    ret = service_manager.iTwins.create_iTwin(iTwins_settings)
    if ret.is_error():
        print("Error while creating iTwin:", ret.error)
        return
    print("iTwin created successfully!")
    print("Created iTwin id : " + ret.value)

if __name__ == "__main__":
    main()
