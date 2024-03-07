import sys
import csv
sys.path.append('/home/abha/abha/umn/rendering_blender/modular/')
import argparse
import os
from cleanup import Utilities
from class_lightning_camera import LightCamera
from create_renders_init import RenderPara
from mesh_generation import MeshGeometry
from class_layers_compositor import ViewLayerCreation
import bpy
import random

# Create a new argument parser
parser = argparse.ArgumentParser(description="Process some arguments.")

# Modify your script to parse arguments after the '--'
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Use argv after the '--'

parser.add_argument('object_filepath', help="Path to the obj file")
parser.add_argument('output_image_path', help="Path to where the final files, will be saved")
parser.add_argument('temp_folder', help="temp folder to save .exr files")
parser.add_argument('csv_path', help="temp folder to save .exr files")
args = parser.parse_args(argv)

camera_pos = [
               [2.0, 2.0, 2.0,1.0471975803375244, 0.0, 2.26892805099487],
               [2.0, 9, .5,1.5277109146118164, 0.03817130625247955, 2.7484679222106934],
               [4.0, 2.0, 3.0,1.0484371185302734, -0.0, 2.0344438552856445],
               [-4.0, 2.0, 5.0,0.7740721702575684, -0.0, -2.0344438552856445],
               [-4.0, 2.0, 1.0,1.4430112838745117, -0.0, -2.0344438552856445],
               [2.0, 9.0, 5.0,1.110205054283142, -0.0, 2.9229238033294678],
               [2.1,-1.7,1.4, 1.2129089832305908, -2.624311309773475e-05, 0.9161228537559509],
               [6,3,0.5,1.517304539680481, 0.019352460280060768, 1.9472476243972778],
               [5,5,5,1.0074996948242188, -0.004958962555974722, 2.235434293746948],
            ]

mount_point_texture_lib = "./data/texture_lib/"
texture_all = ['Abstract_Organic_003','Stylized_Dry_Mud_001','Stylized_Stone_Floor_005','Tiles_046','Paper_Wrinkled_001','Stylized_Rocks_002','Tiles_040']

class Linking:

    def __init__(self, light, camera, object, flat_floor) -> None:
        # self.mod_floor = mod_floor
        self.light = light
        self.camera = camera
        self.object =  object
        self.flat_floor = flat_floor
        

    def clear_collection(self,collection):  #utils
        for obj in collection.objects[:]:
            # Unlink object from the collection
            collection.objects.unlink(obj)

            # Optionally, delete the object completely
            bpy.data.objects.remove(obj)
        return 

    def linking(self):  #links all objects to a collection
        # self.plane_collection.objects.link(self.mod_floor)
        # self.plane_collection.objects.link(self.duplicated_object)
        self.light_collection.objects.link(self.light)
        self.light_collection.objects.link(self.camera)
        self.objects_collection.objects.link(self.object)
        self.objects_collection.objects.link(self.flat_floor)
        return   


    def colls(self):    #tutorial
        ######### Create collection and link onjects
        self.plane_collection = bpy.data.collections.new("plane_col")
        bpy.context.scene.collection.children.link(self.plane_collection)

        self.objects_collection = bpy.data.collections.new("objects_col")
        bpy.context.scene.collection.children.link(self.objects_collection)

        self.light_collection = bpy.data.collections.new("light_col")
        bpy.context.scene.collection.children.link(self.light_collection)

        self.clear_collection(self.objects_collection)
        self.clear_collection(self.plane_collection)
        self.clear_collection(self.light_collection)

        return


def main():

    utilities = Utilities()
    render_para = RenderPara()
    mesh_geometry = MeshGeometry()
    my_layer = "new_view_layer"
    light_camera = LightCamera()

    object_filepath = args.object_filepath
    output_img_folder = args.temp_folder#"./temp/"#args.output_image_path
    # self.save_as_mainfile = bpy.ops.wm.save_as_mainfile #TODO
    # self.file_path2 = file_path2
    isExist = os.path.exists(output_img_folder)
    #print("DOES IT EXIST: ", isExist)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(output_img_folder)

    all_objects = bpy.data.objects
    utilities.remove_objects(all_objects)
    object = mesh_geometry.shapenet_import(object_filepath)

    # object_data = object.data.copy()
    # duplicated_object = bpy.data.objects.new("obj_copy", object_data)

    # mod_floor = mesh_geometry.add_modified_floor()
    # self.mod_floor = self.flat_2()
    # flat_floor = mesh_geometry.add_flat_floor()
    current_texture = random.choice(texture_all)
    # current_texture = "Tiles_046"
    flat_floor = mesh_geometry.apply_pbr_textures(mount_point_texture_lib + current_texture + "/basecolor.jpg", 
                                     mount_point_texture_lib + current_texture+ "/normal.jpg", 
                                     mount_point_texture_lib + current_texture+ "/roughness.jpg", 
                                     mount_point_texture_lib + current_texture+ "/height.png")
    light = light_camera.create_light()

    random_camera_pose = random.choice(camera_pos)
    camera = light_camera.create_camera(random_camera_pose)


    # mod_floor.is_shadow_catcher = True #TODO
    # self.duplicated_object.is_holdout = False# True # default is false anyway #TODO
    # self.mod_floor.hide_render = False #TODO
    # self.mod_floor.visible_camera = True #TODO

    object.visible_shadow = True
    render_para.init_render()
    # print(" the objects",bpy.data.objects.keys())
    linking_coll = Linking(light, camera, object, flat_floor)
    linking_coll.colls()
    linking_coll.linking()
    utilities.clear_node()

    view_layer = ViewLayerCreation(my_layer, ["objects_col", "light_col"], output_img_folder)
    view_layer.depth()
    view_layer.normals()
    view_layer.segmentation()
    view_layer.albedo()
    view_layer.shadow()

    bpy.context.scene.render.film_transparent = True 
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    bpy.ops.render.render(write_still=True)#TODO

    print("Rendered")
    #uuid, object file_path, texture, camerapose
    row_to_append = [" ", object_filepath, current_texture, random_camera_pose]
    csv_file = args.csv_path
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row_to_append)

main()