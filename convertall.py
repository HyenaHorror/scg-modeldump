import subprocess
import os
import sys
from parse import read_material_file
from read_nod import NodModel

def parse_command_line_arguments():
    # Parse command line arguments into input and output paths
    input_path = output_path = ""

    if len(sys.argv) >= 2:
        # Normalize path, assign 1st arg to input_path
        input_path = os.path.normpath(sys.argv[1])
        if len(sys.argv) >= 3:
            # Normalize path, assign 2nd arg to output_path
            output_path = os.path.normpath(sys.argv[2])
        else:
            # Default to current path if 2nd arg absent
            output_path = os.getcwd()
        # Extra arguments beyond the second are ignored
    else:
        # Print usage message and exit if no arguments
        print(f"Usage: {sys.argv[0]} INPUT_PATH [OUTPUT_PATH]")
        sys.exit(1)

    return input_path, output_path

def combine_paths(first, second):
    # Combine and normalize two paths
    return os.path.normpath(os.path.join(first, second))


input_path, output_path = parse_command_line_arguments()
# print(f"Input Path: {input_path}")
# print(f"Output Path: {output_path}")

folder = combine_paths(input_path, "3D/Models")

"""
for file in os.listdir(folder):
    fullpath = os.path.join(folder, file)
    if fullpath.endswith(".nod"):
        with open(fullpath, "rb") as f:
            try:
                with open(fullpath+".obj", "w") as g:
                    nod = NodModel.from_file(f, g)
            except:
                print(fullpath, "failed")"""


def find_all_textures(folderpath):
    textures = {}
    for path, dirs, files in os.walk(folderpath):
        for file in files:
            if file.endswith(".dds"):
                textures[file] = os.path.join(path, file)

    return textures

from shutil import copyfile, SameFileError

mat2texture = {}
textures = find_all_textures(input_path)
print("found all textures")
matpath = combine_paths(input_path, "Materials")
texture_out_path = combine_paths(output_path, "textures")
os.makedirs(texture_out_path, exist_ok=True)
for tex in textures:
    tex_path = textures[tex]
    basename = os.path.basename(tex_path)
    try:
        copyfile(tex_path, os.path.join(texture_out_path, basename))
    except SameFileError:
        pass
    textures[tex] = os.path.join("./textures", basename)


lowercases = {}
for texture in textures:
    lowercases[texture.lower()] = texture

for file in os.listdir(matpath):
    if file.endswith(".nsa"):
        with open(os.path.join(matpath, file), "r") as f:
            materials = read_material_file(f)
        for mat, data in materials.items():
            if "texture" in data:
                tex = data["texture"]
                if tex in textures:
                    mat2texture[mat.lower()] = textures[tex]
                elif tex+".dds" in textures:
                    mat2texture[mat.lower()] = textures[tex+".dds"]
                elif tex.lower() in lowercases:
                    mat2texture[mat.lower()] = textures[lowercases[tex.lower()]]
                elif tex.lower()+".dds" in lowercases:
                    mat2texture[mat.lower()] = textures[lowercases[tex.lower()+".dds"]]

"""for mat in mat2texture:
    path = mat2texture[mat]
    basename = os.path.basename(path)
    copyfile(path, os.path.join("./converted_models/textures", basename))
    mat2texture[mat] = os.path.join("./textures", basename)"""

#import json
#with open("materials.json", "w") as f:
#    json.dump(mat2texture, f, indent=4)

for file in os.listdir(folder):
    #if True:
    #folder = "D:/StarCraftGhost/StarCraft Ghost Xbox Finn Hillbilly/3D/Models"
    #file = "goliath_blue.nod"
    fullpath = os.path.join(folder, file)
    if fullpath.endswith(".nod"):
        basename = os.path.basename(fullpath)

        with open(fullpath, "rb") as f:
            objpath = os.path.join(output_path, basename)
            with open(objpath+".obj", "w") as g:
                with open(objpath+".mtl", "w") as h:
                    try:
                        model = NodModel.from_file(f, g, h, basename+".mtl", mat2texture, textures)
                    except Exception as err:
                        print(fullpath, "failed because", err)
