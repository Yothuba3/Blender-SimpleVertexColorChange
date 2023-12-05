import bpy

bl_info = {
    "name" : "VertColorChange Plugin",
    "author" : "Yothuba",
    "version" : (0,1),
    "blender" : (3,6),
    "location" : "Modeling > Vertex Color Panel",
    "description" : "use in Editing Mode",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UV"
}

# オペレータの定義
class SimpleVertexColorOperator(bpy.types.Operator):
    """選択した頂点の頂点カラーを変更"""
    bl_idname = "mesh.simple_vertex_color_operator"
    bl_label = "Apply Vertex Color"

    def execute(self, context):
        scn = context.scene
        my_tool = scn.my_vertex_color_tool
        color = (my_tool.color[0], my_tool.color[1], my_tool.color[2], 1.0)  # RGBA

        obj = context.active_object
        if obj.type == 'MESH' and obj.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')  # エディットモードからオブジェクトモードに変更

            mesh = obj.data
            if not mesh.vertex_colors:
                mesh.vertex_colors.new()

            color_layer = mesh.vertex_colors.active

            for poly in mesh.polygons:
                for idx in poly.loop_indices:
                    loop_vert_idx = mesh.loops[idx].vertex_index
                    if mesh.vertices[loop_vert_idx].select:
                        color_layer.data[idx].color = color

            bpy.ops.object.mode_set(mode='EDIT')  # 元のエディットモードに戻す

        return {'FINISHED'}

# プロパティグループの定義
class VertexColorProperties(bpy.types.PropertyGroup):
    color : bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )

# パネルの定義
class VertexColorPanel(bpy.types.Panel):
    bl_label = "Vertex Color Panel"
    bl_idname = "MESH_PT_vertex_color_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_tool = scene.my_vertex_color_tool

        layout.prop(my_tool, "color", text="")
        layout.operator("mesh.simple_vertex_color_operator")
        
def menu_func(self,context):
    self.layout.operator(SimpleVertexColorOperator.bl_idname)

# プラグインの登録と解除
def register():
    bpy.utils.register_class(VertexColorProperties)
    bpy.utils.register_class(SimpleVertexColorOperator)
    bpy.utils.register_class(VertexColorPanel)
    bpy.types.Scene.my_vertex_color_tool = bpy.props.PointerProperty(type=VertexColorProperties)

def unregister():
    bpy.utils.unregister_class(VertexColorProperties)
    bpy.utils.unregister_class(SimpleVertexColorOperator)
    bpy.utils.unregister_class(VertexColorPanel)
    del bpy.types.Scene.my_vertex_color_tool

if __name__ == "__main__":
    register()
