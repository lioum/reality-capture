import reality_capture.specifications.segmentation2d as segmentation2d

s2d_inputs = segmentation2d.Segmentation2DInputs(photos="401975b7-0c0a-4498-5896-84987921f4bb",
                                                 photoSegmentationDetector="08342927-859c-4563-a4b8-6c6cfb7d5bb3")
s2d_outputs = [segmentation2d.Segmentation2DOutputsCreate.SEGMENTATION2D,
               segmentation2d.Segmentation2DOutputsCreate.SEGMENTED_PHOTOS]
s2d_options = segmentation2d.Segmentation2DOptions()
s2ds = segmentation2d.Segmentation2DSpecificationsCreate(inputs=s2d_inputs, outputs=s2d_outputs, options=s2d_options)
