import bpy

class LightCamera:
    def create_light(self): #scene setup

        # Create a new light datablock
        light_data = bpy.data.lights.new(name="PointLight", type='POINT')

        # Set the light's energy
        light_data.energy = 2000

        # Create a new object with the light datablock
        light_object = bpy.data.objects.new(name="PointLight", object_data=light_data)

        # Link the light object to the current scene
        bpy.context.collection.objects.link(light_object)

        # Set the light's location
        light_pos = (4, 2, 3)  # Example position, replace with your desired coordinates
        light_object.location = light_pos
        return light_object
    
    def create_camera(self):    #scene setup

        cam1 = bpy.data.cameras.new("Camera")
        
        # create the first camera object
        cam_obj1 = bpy.data.objects.new("Camera", cam1)
        cam_obj1.location = (2.0, 2.0, 2.0)
        cam_obj1.rotation_euler = (1.0471975803375244, 0.0, 2.26892805099487)

        bpy.context.scene.camera = cam_obj1
        return cam_obj1