import bpy
import bmesh



def set_selected_attribute(domain, attr_name, value, default_value=None):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    elements_map = {"POINT": bm.verts, "EDGE": bm.edges, "FACE": bm.faces}

    elements = elements_map.get(domain)
    if elements is None:
        return
    
    layer = elements.layers.float.get(attr_name)
    is_new_layer = layer is None
    if is_new_layer:
        layer = elements.layers.float.new(attr_name)

    default_assign_value = float(value if default_value is None else default_value)

    if is_new_layer:
        for elem in elements:
            elem[layer] = default_assign_value

    for elem in elements:
        if elem.select:
            elem[layer] = float(value)
            
    bmesh.update_edit_mesh(me, loop_triangles=False)



def on_slider_update(self, context):
    set_selected_attribute("FACE", "DemoValue", self.SliderValue)

bpy.types.Object.SliderValue = bpy.props.FloatProperty(
    name="Float value",
    default=0.0,
    min=0.0,
    max=25.0,
    update=on_slider_update,
)

class DemoPanel(bpy.types.Panel):
    bl_label = "Demo Panel"
    bl_idname = "OBJECT_PT_demo_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Demo'
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.active_object, "SliderValue")


