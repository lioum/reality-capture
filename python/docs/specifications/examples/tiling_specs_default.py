import reality_capture.specifications.tiling as tiling

tiling_inputs = tiling.TilingInputs(scene="401975b7-0c0a-4498-8896-84987921f4bb")
tiling_outputs = [tiling.TilingOutputsCreate.REFERENCE_MODEL]
tiling_options = tiling.TilingOptions()
tiling_specs = tiling.TilingSpecificationsCreate(inputs=tiling_inputs, outputs=tiling_outputs, options=tiling_options)
