import bpy

class LightCamera:
    def create_light(self): #scene setup

        # Create a new light datablock
        light_data = bpy.data.lights.new(name="PointLight", type='POINT')

        # Set the light's energy
        light_data.energy = 5000

        # Create a new object with the light datablock
        light_object = bpy.data.objects.new(name="PointLight", object_data=light_data)

        # Link the light object to the current scene
        bpy.context.collection.objects.link(light_object)

        # Set the light's location
        light_pos = (4, 2, 3)  # Example position, replace with your desired coordinates
        light_object.location = light_pos
        return light_object
    
    def create_camera(self, camera_pose):    #scene setup

        cam1 = bpy.data.cameras.new("Camera")
        
        # create the first camera object
        cam_obj1 = bpy.data.objects.new("Camera", cam1)
        cam_obj1.location = (camera_pose[0],camera_pose[1],camera_pose[2])
        cam_obj1.rotation_euler = (camera_pose[3],camera_pose[4],camera_pose[5])

        bpy.context.scene.camera = cam_obj1
        return cam_obj1