# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os
import json
from pathlib import Path
from contextscene.contextscene import ContextSceneModel, FilePath
'''
Create a json Contextscene base on a folder with a mesh inside

input folder is the path where the mesh is stored.
output file is where to save the created context scene
'''

INPUT_FOLDER = "C:/Path/to/mesh/folder"
OUTPUT_FILE = "C:/Path/to/output/ContextScene.json"
FORMAT_3D = [".opc", ".3sm", ".3mx"]


def main():
    # Initialize empty ContextScene
    context_scene = ContextSceneModel()
    # Initialize empty meshes dictionnay
    context_scene.mesh_collection.meshes = {}

    # Create reference and add files
    for _path in Path(INPUT_FOLDER).rglob("*"):
        if _path.is_file() and _path.suffix.lower() in FORMAT_3D:
            ref_id = context_scene.add_or_get_reference(_path.parent)
            mesh_id = len(context_scene.mesh_collection.meshes)
            meshes = context_scene.mesh_collection.meshes
            meshes[mesh_id] = {"name":f"{_path.stem}", "path":str(FilePath(ref_id,_path.name))}
            context_scene.mesh_collection.meshes = meshes # This will enforce validation since dictionnaries are mutable.
            if _path.suffix.lower() == ".3mx":
                data_3mx = json.loads(_path.read_text())
                srs_id = context_scene.add_or_get_spatial_reference(data_3mx["layers"][0]["SRS"])
                context_scene.mesh_collection.srs_id = srs_id

    # Save the context scene
    Path(OUTPUT_FILE).write_text(context_scene.serialize())

if __name__ == '__main__':
    main()
