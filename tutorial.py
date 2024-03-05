import sys
# print(sys.path)
sys.path.append('/home/abha/abha/umn/rendering_blender/modular/')
import argparse
import os
from cleanup import Utilities
from class_lightning_camera import LightCamera
from create_renders_init import RenderPara
from mesh_generation import MeshGeometry
from class_layers_compositor import ViewLayerCreation
import bpy

print("PRINT1")

# parser = argparse.ArgumentParser()
# parser.add_argument('object_filepath', nargs='?', help="Path to the obj file")
# # parser.add_argument('height',nargs='?', help="height in mm")
# parser.add_argument('output_image_path', nargs='?', help="Path to where the final files, will be saved")
# args = parser.parse_args()


# Create a new argument parser
parser = argparse.ArgumentParser(description="Process some integers.")

# Modify your script to parse arguments after the '--'
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Use argv after the '--'

parser.add_argument('object_filepath', help="Path to the obj file")
parser.add_argument('output_image_path', help="Path to where the final files, will be saved")
args = parser.parse_args(argv)
print("PRINT2")

# all_objects = bpy.data.objects


class Linking:

    def __init__(self, mod_floor, light, camera, object, flat_floor) -> None:
        self.mod_floor = mod_floor
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
        self.plane_collection.objects.link(self.mod_floor)
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


    # shadow_view_layer = ViewLayerCreation("ShadowCatcherLayer", [])
    object_filepath = args.object_filepath
    output_img_folder = args.output_image_path
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

    mod_floor = mesh_geometry.add_modified_floor()
    # self.mod_floor = self.flat_2()
    flat_floor = mesh_geometry.add_flat_floor()
    light = light_camera.create_light()
    camera = light_camera.create_camera()

    mod_floor.is_shadow_catcher = True
    # self.duplicated_object.is_holdout = False# True # default is false anyway
    # self.duplicated_object.visible_shadow = True

    flat_floor.is_shadow_catcher = True
    # self.duplicated_object.is_holdout = False# True
    # self.object.visible_shadow = True
    # self.object.visible_shadow = False
    # self.mod_floor.visible_shadow = True
    # self.mod_floor.hide_render = False
    # self.mod_floor.visible_camera = True #TODO
    object.visible_shadow = True
    render_para.init_render()
    # print(" the objects",bpy.data.objects.keys())
    # self.saving_blends()
    linking_coll = Linking(mod_floor, light, camera, object, flat_floor)
    linking_coll.colls()
    linking_coll.linking()
    utilities.clear_node()
    
    # self.shadow_layer()
    # self.new_view_layer()
    
    
    # self.shading() # Problem
    view_layer = ViewLayerCreation(my_layer, ["objects_col", "light_col"], output_img_folder)
    new_view_layer = bpy.context.scene.view_layers[my_layer]
    new_view_layer.use_pass_diffuse_color = True
    new_view_layer.use_pass_z = True
    new_view_layer.use_pass_normal = True
    new_view_layer.use_pass_object_index = True    
    new_view_layer.pass_alpha_threshold = 0.05
    view_layer.depth()
    view_layer.normals()
    view_layer.segmentation()
    view_layer.albedo()

    list_layers = [layer.name for layer in bpy.context.scene.view_layers]
    print("the layers at the end: ",list_layers)
    bpy.context.scene.render.film_transparent = True 
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    bpy.ops.render.render(write_still=True)#TODO
    print("Rendered")

main()