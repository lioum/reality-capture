# Copyright (c) Bentley Systems, Incorporated. All rights reserved.
# See LICENSE.md in the project root for license terms and full copyright notice.

import os
import json
from contextscene.contextscene import ContextSceneModel
from pathlib import Path
'''
This script only open the context scene in order to create the object Context scene than save it again

'''

INPUT = "C:/Path/To/existing/ContextScene.json"
OUTPUT = "P:/Path/To/output/ContextScene.json"


def main():

    cs = ContextSceneModel.deserialize(Path(INPUT).read_text())
    
    cs_json_dumps = cs.serialize()
    Path(OUTPUT).write_text(cs_json_dumps)

if __name__ == '__main__':
    main()
