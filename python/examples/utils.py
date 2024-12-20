# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

# Utils functions for the examples

import reality_apis.iTwins.itwins as iTwins
import reality_apis.DataTransfer.reality_data_transfer as DataTransfer
import reality_apis.CCS.context_capture_service as CCS
import reality_apis.RC.reality_conversion_service as RC
import reality_apis.RDAS.reality_data_analysis_service as RDAS

from token_factory.token_factory import ClientInfo, SpaDesktopMobileTokenFactory

# Class to manage all the services that can be requested in the examples
class ServiceManager:
    def __init__(self) -> None:
        self.iTwins = None # Service to create iTwins
        self.management = None # Service to upload and download data
        self.modeling = None # Service to submit Modeling jobs
        self.conversion = None # Service to convert data
        self.analysis = None # Service to submit Analysis jobs

# Function for authentication with Single Page Application (SPA) client. Used for React web app. To create a client, see here https://developer.bentley.com/my-apps/
def authenticate_with_spa_client(client_id: str):
    scope_set = {
        "itwin-platform"
    }

    client_info = ClientInfo(client_id, scope_set)
    token_factory = SpaDesktopMobileTokenFactory(client_info)

    service_manager = ServiceManager()

    service_manager.iTwins = iTwins.iTwinsApiWrapper(token_factory)
    service_manager.management = DataTransfer.RealityDataTransfer(token_factory)
    service_manager.modeling = CCS.ContextCaptureService(token_factory)
    service_manager.conversion = RC.RealityConversionService(token_factory)
    service_manager.analysis = RDAS.RealityDataAnalysisService(token_factory)

    # adding hook to follow upload and download progress
    service_manager.management.set_progress_hook(DataTransfer.example_hook)
    return service_manager

# Function for authentication with Desktop/Mobile client. Used for desktop applications. To create a client, see here https://developer.bentley.com/my-apps/
def authenticate_with_desktop_client(client_id):
    # TODO
    return

# Function for authentication with Service client. Used for automated tasks. To create a client, see here https://developer.bentley.com/my-apps/
def authenticate_with_service_client(client_id):
    # TODO
    return

