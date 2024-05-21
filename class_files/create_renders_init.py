import bpy



class RenderPara:

    def adjust_modifier_visibility(self, scene, view_layer):     #removes gridline (visibility of the modifier for another layer)
    # Example: Toggle the Wireframe modifier based on view layer name
        obj = self.mod_floor
        view_layer = bpy.context.scene.view_layers
        if obj and "Wireframe" in obj.modifiers:
            for layer in bpy.context.scene.view_layers:

        # Example condition: if view layer name contains "Special", show the modifier
                obj.modifiers["Wireframe"].show_render = ("ShadowCatcherLayer" in layer.name)

    def init_render(self):      #setting up render parameters
        bpy.context.scene.render.engine = 'CYCLES'

        # Set maximum render samples
        bpy.context.scene.cycles.samples = 100  # You can change this value as needed
        bpy.context.scene.cycles.preview_samples = 100

        # # Set the resolution of the rendered image
        bpy.context.scene.render.resolution_x = 1280  # Width, change as needed
        bpy.context.scene.render.resolution_y = 720 # Height, change as needed

        # bpy.context.scene.render.resolution_percentage = 10
        # Register the handler (remove the previous one to avoid duplicates)
        bpy.app.handlers.render_init.clear() 
        # bpy.app.handlers.render_init.append(self.adjust_modifier_visibility) # TODO
        return