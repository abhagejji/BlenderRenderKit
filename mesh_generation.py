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
        self.plane = plane_flat
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
    
    def apply_pbr_textures(self,base_color_path, normals_path, roughness_path, displacement_path):
        # Create a plane for the floor
        bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=True, align='WORLD', location=(0, 0, -0.01))
        plane = bpy.context.object
        plane.name = "myFloor"
        # Subdivide the plane for more geometry
        bpy.ops.mesh.subdivide(number_cuts=10)
        bpy.ops.object.editmode_toggle()
        # bpy.context.object = self.plane
        # plane = bpy.data.objects.get('flat_floor')
        # Add a subdivision surface modifier for displacement
        bpy.ops.object.modifier_add(type='SUBSURF')
        plane.modifiers['Subdivision'].levels = 7
        plane.modifiers['Subdivision'].render_levels = 7
        
        # Apply the modifier
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        
        # Create a new material
        mat = bpy.data.materials.new(name="PBR_Material")
        
        
        # Enable 'Use Nodes':
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create Principled BSDF
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = 0,0
        
        # Load and link base color texture
        base_color_img = bpy.data.images.load(base_color_path)
        base_color_texture = nodes.new(type='ShaderNodeTexImage')
        base_color_texture.image = base_color_img
        links.new(base_color_texture.outputs['Color'], bsdf.inputs['Base Color'])
        
        # Load and link normal map
        normal_img = bpy.data.images.load(normals_path)
        normal_map = nodes.new(type='ShaderNodeNormalMap')
        normal_texture = nodes.new(type='ShaderNodeTexImage')
        normal_texture.image = normal_img
        links.new(normal_texture.outputs['Color'], normal_map.inputs['Color'])
        links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
        
        # Load and link roughness texture
        roughness_img = bpy.data.images.load(roughness_path)
        roughness_texture = nodes.new(type='ShaderNodeTexImage')
        roughness_texture.image = roughness_img
        links.new(roughness_texture.outputs['Color'], bsdf.inputs['Roughness'])
        
        # Add displacement
        displacement_img = bpy.data.images.load(displacement_path)
        displacement_texture = nodes.new('ShaderNodeTexImage')
        displacement_texture.image = displacement_img
        displacement = nodes.new(type='ShaderNodeDisplacement')
        links.new(displacement_texture.outputs['Color'], displacement.inputs['Height'])
        
        # Link displacement to material output
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(displacement.outputs['Displacement'], material_output.inputs['Displacement'])
        
        # Set material settings for displacement
        mat.cycles.displacement_method = 'BOTH'

        # Link BSDF to material output
        links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])
        plane.data.materials.append(mat)
   
        return plane
    