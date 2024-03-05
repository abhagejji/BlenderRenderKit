import bpy


class MeshGeometry:
    def shapenet_import(self,object_filepath):  #importing object file from shapenet dataset
        # bpy.ops.import_scene.obj(filepath=object_filepath)

        bpy.ops.wm.obj_import(filepath=object_filepath)

        # bpy.context.view_layer.objects.active = active_object
        # Get a list of all the imported objects
        objs = [obj for obj in bpy.context.selected_objects]

        for obj in objs:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        # # # Rename the merged object
        bpy.context.active_object.name = "myMergedMesh"
        mesh_obj = bpy.data.objects["myMergedMesh"]
        bbox = mesh_obj.bound_box
    
        # Calculate  the dimensions of the bounding box
        x_size = bbox[6][0] - bbox[0][0]
        z_size = bbox[6][1] - bbox[0][1]
        y_size = bbox[6][2] - bbox[0][2]
        scale_factor = 1#2 / max(x_size, y_size, z_size)
        mesh_obj.scale = (scale_factor,scale_factor,scale_factor)
        mesh_obj.location = (0,0, -1*bbox[0][1])
        # print(bbox[0], bbox[6])
        # raise
        # bpy.ops.mesh.primitive_cube_add(size=1, scale=(x_size, y_size, z_size), location=mesh_obj.location)
        # mesh_obj.location = (0,0,-0.01)
        return mesh_obj

    def add_modified_floor(self):   #creating floor #1
            
        # Create a plane for the floor
        bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=True, align='WORLD', location=(0, 0, -0.01))
        plane = bpy.context.object
        plane.name = "myFloor"
        # Subdivide the plane for more geometry
        bpy.ops.mesh.subdivide(number_cuts=10)
        bpy.ops.object.editmode_toggle()

        # Add noise-based displacement for an irregular pattern
        bpy.ops.object.modifier_add(type='DISPLACE')
        displace_modifier = plane.modifiers['Displace']
        displace_modifier.strength = 0.5

        # Create a Clouds texture for displacement
        bpy.ops.texture.new()
        noise_texture = bpy.data.textures.new("NoiseTexture", type='CLOUDS')
        noise_texture.noise_scale = 2.0
        displace_modifier.texture = noise_texture

        # Apply the displacement modifier
        bpy.ops.object.modifier_apply(modifier="Displace")

        # Triangulate the mesh for a non-square pattern
        bpy.ops.object.modifier_add(type='TRIANGULATE')
        bpy.ops.object.modifier_apply(modifier="Triangulate")

        # Smooth the mesh
        bpy.ops.object.modifier_add(type='SMOOTH')
        smooth_modifier = plane.modifiers['Smooth']
        smooth_modifier.iterations = 10  # Adjust as needed for smoothness
        bpy.ops.object.modifier_apply(modifier="Smooth")

        # Add a Subdivision Surface modifier for roundness
        bpy.ops.object.modifier_add(type='SUBSURF')
        subsurf_modifier = plane.modifiers['Subdivision']
        subsurf_modifier.levels = 2  # Adjust for desired roundness
        bpy.ops.object.modifier_apply(modifier="Subdivision")

        # Convert to a wireframe with thickness for through holes
        bpy.ops.object.modifier_add(type='WIREFRAME')
        wireframe_modifier = plane.modifiers['Wireframe']
        wireframe_modifier.thickness = 0.05
        wireframe_modifier.use_boundary = True
        wireframe_modifier.use_replace = True

        # print("Floor with smoother and rounder mesh pattern created successfully.")


        return plane
        
    def add_flat_floor(self):   #creating floor #2
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, -0.01),scale=(17, 17, 17))
        plane_flat = bpy.context.object
        plane_flat.scale = (20,20,10)
        plane_flat.name = "flat_floor"
        return plane_flat

    def create_ocean_floor(self):   #creating floor #3

        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),scale=(5, 5, 5))
        plane = bpy.context.object
        plane.name = "myFloor"
        bpy.data.objects["myFloor"].scale = (15,15,1)

        wave_modifier = plane.modifiers.new(name="new", type='OCEAN')
        wave_modifier.depth = 10#200
        wave_modifier.viewport_resolution = 10
        wave_modifier.size = 1
        wave_modifier.spatial_size = 100
        wave_modifier.wave_scale = 1
        bpy.ops.object.modifier_apply(modifier="new",object=plane)
        return plane