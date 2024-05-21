import bpy


class ViewLayerCreation:
    def __init__(self, view_layer_name, collection_link, output_img_folder) -> None:
        self.output_img_folder = output_img_folder
        self.view_layer_name = view_layer_name
        self.tree = bpy.context.scene.node_tree
        bpy.context.scene.view_layers.new(name=self.view_layer_name)
        self.current_layer = bpy.context.scene.view_layers[self.view_layer_name]
        bpy.context.window.view_layer = self.current_layer
    
        lc = self.current_layer.layer_collection
        # list_colls = [coll.name for coll in lc.children]
        # print(" the childern at the end", list_colls)
        for coll in lc.children:
            coll.exclude = True

        for name in collection_link:
            for coll in lc.children:
                if name == coll.name:
                    coll.exclude = False

        self.connect_compositor_node()

        
    def connect_compositor_node(self):
        render_layers_node = self.tree.nodes.new(type='CompositorNodeRLayers')
        render_layers_node.layer = self.view_layer_name  # Set to the name of the new view layer
        render_layers_node.name = "RLayers_all_" + self.view_layer_name
        # print("render output",tree.nodes['RLayers_all'].outputs.keys())
        output_node =  self.tree.nodes.new(type="CompositorNodeOutputFile")#CompositorNodeComposite
        # print("HERE HERE render outputn depth",render_layers_node.outputs.keys())
        self.tree.links.new(render_layers_node.outputs['Image'], output_node.inputs['Image'])

        output_node.base_path = self.output_img_folder  # Set the base save path
        output_node.file_slots[0].path = "colors"
        output_node.format.file_format = "OPEN_EXR"
        # self.mod_floor.modifiers["Wireframe"].show_render = False
        return

    def depth(self):  # either layer or a function in render or composition class
        self.current_layer.use_pass_z = True
        # OUTPUT
        output_file = self.tree.nodes.new("CompositorNodeOutputFile")
        output_file.name = "OutFile_depth"
        output_file.base_path = self.output_img_folder
        output_file.format.file_format = "OPEN_EXR"
        output_file.file_slots[0].path = "depth"
        
        # Add a Normalize node
        normalize_node = self.tree.nodes.new(type="CompositorNodeNormalize")
        
        # Link the Depth output to the Normalize node, and then to the Output node
        depth_output = self.tree.nodes["RLayers_all_" + self.view_layer_name].outputs['Depth']
        self.tree.links.new(depth_output, normalize_node.inputs[0])
        self.tree.links.new(normalize_node.outputs[0], output_file.inputs['Image'])

        return

    def normals(self):  #either layer or a function in render or composition class
        self.current_layer.use_pass_normal = True
        #OUTPUT
        output_file_normals = self.tree.nodes.new("CompositorNodeOutputFile")
        output_file_normals.name = "OutFile_normals"
        output_file_normals.base_path = self.output_img_folder
        output_file_normals.format.file_format = "OPEN_EXR"
        output_file_normals.file_slots[0].path = "normals"
        #LINK
        self.tree.links.new(self.tree.nodes["RLayers_all_" + self.view_layer_name].outputs["Normal"], self.tree.nodes['OutFile_normals'].inputs['Image'])
        return

    def albedo(self):   #either layer or a function in render or composition class
        self.current_layer.use_pass_diffuse_color = True
        output_file_normals = self.tree.nodes.new("CompositorNodeOutputFile")
        output_file_normals.name = "OutFile_albedo"
        output_file_normals.base_path = self.output_img_folder
        output_file_normals.format.file_format = "OPEN_EXR"
        output_file_normals.file_slots[0].path = "albedo"
        #LINK
        self.tree.links.new(self.tree.nodes["RLayers_all_" + self.view_layer_name].outputs["DiffCol"], self.tree.nodes['OutFile_albedo'].inputs['Image'])
        return

    def segmentation(self): #either layer or a function in render or composition class
        self.current_layer.use_pass_object_index = True
        self.current_layer.pass_alpha_threshold = 0.05  
        for index, obj in enumerate(bpy.data.objects):
            obj.pass_index = index + 1
        output_file_normals = self.tree.nodes.new("CompositorNodeOutputFile")
        output_file_normals.name = "OutFile_segment"
        output_file_normals.base_path = self.output_img_folder
        output_file_normals.format.file_format = "OPEN_EXR"
        output_file_normals.file_slots[0].path = "segment"
        #LINK
        self.tree.links.new(self.tree.nodes["RLayers_all_" + self.view_layer_name].outputs["IndexOB"], self.tree.nodes['OutFile_segment'].inputs['Image'])
        
        return
    
    def shadow(self):   #either layer or a function in render or composition class
        self.current_layer.use_pass_shadow = True # Not avaliable for blender 4 onwards
        output_file_normals = self.tree.nodes.new("CompositorNodeOutputFile")
        output_file_normals.name = "OutFile_shadow"
        output_file_normals.base_path = self.output_img_folder
        output_file_normals.format.file_format = "OPEN_EXR"
        output_file_normals.file_slots[0].path = "shadow"
        #LINK
        self.tree.links.new(self.tree.nodes["RLayers_all_" + self.view_layer_name].outputs["Shadow"], self.tree.nodes['OutFile_shadow'].inputs['Image'])
     
