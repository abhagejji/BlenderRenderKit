#ONE OFF FUNCTIONS THAT BASICALLY DO CLEANUP

import bpy

class Utilities:
    def remove_objects(self, scene_objects):
        """
        Remove a collection of objects from the scene.
        :param scene_objects: A collection of objects to be removed.
        """
        for obj in scene_objects[:]:  # Iterate over a copy of the list
            bpy.data.objects.remove(obj, do_unlink=True)


    def clear_node(self):   #utils

        bpy.context.scene.render.use_compositing = True
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        for node in tree.nodes:
            tree.nodes.remove(node)
        tree.nodes.clear()

        return