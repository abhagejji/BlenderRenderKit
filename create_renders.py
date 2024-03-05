# import pdb
import bpy 
import sys
import os
import csv
# import mathutils
# import argparse

sys.path.append(os.path.basename(bpy.data.filepath))
# import create_scene_advance as scene
# import parameters_adv as par

mount_point = "/home/abha/abha/umn/mono_depth/resources_data/selected_obj_files/"

# with open("./object_loc_output_loc.csv", 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
    
#     # Skip header 
#     next(csv_reader)
#     for index, row in enumerate(csv_reader):
#         #object_filepath,output_blend_paths
#         object_filepath = mount_point  + str(row[1])
#         output_folder = save_data  #+ str(row[0])
#         scene.direct_renders(object_filepath,output_folder)
#         arguments = str(object_filepath)+","+str(output_folder)+")"
#         os.system(f"blender -b -P scene.direct_renders(" + arguments )
#         break
        
# print("-----------------------------------------------------------------------")


object_filepath = mount_point  + "03710193/f8ebd72bdd49a43b8ad4a36593b38a9e/model.obj"
output_folder = "/home/abha/abha/umn/rendering_blender/modular/temp/"  #+ str(row[0])
# scene.direct_renders(object_filepath,output_folder)
arguments = str(object_filepath)+" "+str(output_folder)
# print(f'blender -P tutorial.py -- '+ arguments)

# breakpoint()
os.system(f'blender -b -P tutorial.py -- '+ arguments)

# os.system(f'blender -b -P create_scene_advance.py -- '+ arguments)
# os.system(f'python post_processing.py')