# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os
import json
from pathlib import Path
from contextscene.contextscene import ContextSceneModel, FilePath
'''
Create a json Contextscene base on a folder with picture

input folder is the path where the picture are stored. It could be a folder containing folder with pictures
output folder is where to save the created context scene
segmentation folder, needed if SEGMENTED_CONTEXT_SCENE is true. It is the location of you 16bits png mask
labels file is a json file containing references to the classes of the segmented masks

Example of label file :
{
    "0" : {
        "Name" : "background"
    },
    "1" : {
        "Name" : "crack"
    }
}
'''

INPUT_FOLDER = "C:/Path/to/images/folder"
SEGMENTATION_FOLDER = "C:/Path/to/masks"
LABEL_FILE = "C:/Path/to/label_file.json"
OUTPUT_FILE = "C:/Path/to/output/ContextScene.json"
PICTURE_FORMAT = ["jpg", "png", "jpeg"]

def main():

 # Initialize empty ContextScene
    context_scene = ContextSceneModel()
    # Initialize empty meshes dictionnay
    context_scene.mesh_collection.meshes = {}

    # Create reference and add files
    if INPUT_FOLDER:
        for _path in Path(INPUT_FOLDER).rglob("*"):
            if _path.is_file() and _path.suffix.lower() in PICTURE_FORMAT:
                ref_id = context_scene.add_or_get_reference(_path.parent)
                # We can use a helper method to add a new item in the dictionnary, or treat context_scene.photo_collection like a dictionnary.
                photo_id = len(context_scene.photo_collection.photos)
                context_scene.photo_collection.photos[photo_id] = ContextSceneModel.PhotoCollectionModel.PhotoModel(image_path=str(FilePath(ref_id,_path.name)))
    
    if LABEL_FILE:
       # If the labels file is in this format Dict[str, ContextSceneModel.Annoation.LabelModel] 
       context_scene.annotations.labels =  json.loads(Path(LABEL_FILE).read_text())

    if SEGMENTATION_FOLDER:
        for _path in Path(SEGMENTATION_FOLDER).rglob("*"):
            if _path.is_file() and _path.suffix.lower() in PICTURE_FORMAT:
                ref_id = context_scene.add_or_get_reference(_path.parent)
                # We can use a helper method to add a new item in the dictionnary, or treat context_scene.photo_collection like a dictionnary.
                segmentation_2d_id = len(context_scene.annotations.segmentation_2d)
                context_scene.annotations.segmentation_2d[segmentation_2d_id] = {"image_path":f"{ref_id}:{_path.name}"}

    # Save the context scene
    Path(OUTPUT_FILE).write_text(context_scene.serialize())
    

if __name__ == '__main__':
    main()
