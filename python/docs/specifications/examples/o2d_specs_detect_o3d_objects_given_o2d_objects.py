import reality_capture.specifications.objects2d as objects2d

o2d_inputs = objects2d.Objects2DInputs(photos="587a14fd-305a-474c-b037-26d4ee8829d9",
                                       objects2D="63376f37-6ud5-466b-b361-9fc3623125f8")
o2d_outputs = [objects2d.Objects2DOutputsCreate.OBJECTS3D]
o2d_options = objects2d.Objects2DOptions()
o2ds = objects2d.Objects2DSpecificationsCreate(inputs=o2d_inputs, outputs=o2d_outputs, options=o2d_options)
