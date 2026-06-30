import bpy
import os

FACE_MESH_SUFFIX = "_Face"
FACE_MATERIAL_NAME = "ZZZ Shader Face"

LIGHTMAP_GROUPS = [
    (
        "Female",
        [
            ("1", "Female_Face_Lightmap.png"),
            ("2", "Female_Face_Lightmap_02.png"),
            ("FX", "Female_Face_lightmap_FX.png"),
        ],
    ),
    (
        "Male",
        [
            ("1", "Male_Face_01_Lightmap.png"),
            ("2", "Male_Face_02_Lightmap.png"),
        ],
    ),
    (
        "Monster",
        [
            ("1", "Monster_Face_01_Lightmap.png"),
        ],
    ),
    (
        "NPC Face",
        [
            ("Child", "NPC_Face_Child_Lightmap.png"),
            ("Older", "NPC_Face_Older_Lightmap.png"),
        ],
    ),
    (
        "NPC Furry",
        [
            ("1", "NPC_Furry_Face01_Lightmap.png"),
            ("2", "NPC_Furry_Face02_Lightmap.png"),
            ("3", "NPC_Furry_Face03_Lightmap.png"),
        ],
    ),
]

def normalize_name(name):
    return name.lower().replace(" ", "").replace("_", "").replace(".", "").replace("-", "")

def clean_image_name(name):
    return os.path.basename(name).lower()

def find_image_by_name(image_name):
    target = clean_image_name(image_name)

    for image in bpy.data.images:
        if clean_image_name(image.name) == target:
            return image

    for image in bpy.data.images:
        if image.filepath and clean_image_name(image.filepath) == target:
            return image

    for image in bpy.data.images:
        if image.filepath and clean_image_name(bpy.path.abspath(image.filepath)) == target:
            return image

    return None

def find_face_mesh():
    obj = bpy.context.object

    if obj and obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
        return obj

    for obj in bpy.context.selected_objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    return None

def get_face_material(face_obj):
    if len(face_obj.material_slots) < 1:
        raise RuntimeError(f'{face_obj.name} does not have material slot 1.')

    material = face_obj.material_slots[0].material

    if material is None:
        raise RuntimeError(f'Material slot 1 on {face_obj.name} is empty.')

    if normalize_name(material.name) != normalize_name(FACE_MATERIAL_NAME):
        raise RuntimeError(f'Material slot 1 is "{material.name}", not "{FACE_MATERIAL_NAME}".')

    if material.node_tree is None:
        raise RuntimeError(f'{material.name} does not use nodes.')

    return material

def node_matches_face_lightmap(node):
    names = [
        node.name,
        getattr(node, "label", ""),
    ]

    if node.type == "GROUP" and node.node_tree is not None:
        names.append(node.node_tree.name)

    for name in names:
        normalized = normalize_name(name)

        if "facelightmap" in normalized:
            return True

    return False

def image_node_matches_lightmap(node):
    names = [
        node.name,
        getattr(node, "label", ""),
    ]

    if node.image is not None:
        names.append(node.image.name)
        names.append(node.image.filepath)

    for name in names:
        normalized = normalize_name(name)

        if "face" in normalized and "lightmap" in normalized:
            return True

        if "facelightmap" in normalized:
            return True

    return False

def find_upstream_image_nodes(node, found, visited_nodes):
    if node in visited_nodes:
        return

    visited_nodes.add(node)

    if node.type == "TEX_IMAGE":
        found.append(node)
        return

    for input_socket in node.inputs:
        for link in input_socket.links:
            find_upstream_image_nodes(link.from_node, found, visited_nodes)

def find_image_nodes_connected_to_group_output(node_tree):
    found = []

    for node in node_tree.nodes:
        if node.type == "GROUP_OUTPUT":
            for input_socket in node.inputs:
                for link in input_socket.links:
                    find_upstream_image_nodes(link.from_node, found, set())

    return found

def collect_lightmap_image_nodes_from_tree(node_tree, found, visited_trees):
    if node_tree in visited_trees:
        return

    visited_trees.add(node_tree)

    for node in node_tree.nodes:
        if node.type == "TEX_IMAGE" and image_node_matches_lightmap(node):
            found.append(node)

        if node.type == "GROUP" and node.node_tree is not None:
            if node_matches_face_lightmap(node):
                output_image_nodes = find_image_nodes_connected_to_group_output(node.node_tree)

                if output_image_nodes:
                    for image_node in output_image_nodes:
                        if image_node not in found:
                            found.append(image_node)

                for inner_node in node.node_tree.nodes:
                    if inner_node.type == "TEX_IMAGE":
                        if inner_node not in found:
                            found.append(inner_node)

            collect_lightmap_image_nodes_from_tree(node.node_tree, found, visited_trees)

def find_face_lightmap_image_nodes(material):
    found = []
    collect_lightmap_image_nodes_from_tree(material.node_tree, found, set())

    unique_found = []

    for node in found:
        if node not in unique_found:
            unique_found.append(node)

    if unique_found:
        return unique_found

    all_image_nodes = []

    def collect_all_image_nodes(node_tree, visited_trees):
        if node_tree in visited_trees:
            return

        visited_trees.add(node_tree)

        for node in node_tree.nodes:
            if node.type == "TEX_IMAGE":
                all_image_nodes.append(node)

            if node.type == "GROUP" and node.node_tree is not None:
                collect_all_image_nodes(node.node_tree, visited_trees)

    collect_all_image_nodes(material.node_tree, set())

    image_node_names = []

    for node in all_image_nodes:
        current_image = node.image.name if node.image else "No image"
        image_node_names.append(f'{node.name} / {current_image}')

    raise RuntimeError(f'Could not find a face lightmap image texture node. Found image nodes: {image_node_names}')

def set_face_lightmap_image(image_name):
    image = find_image_by_name(image_name)

    if image is None:
        raise RuntimeError(f'Image "{image_name}" was not found in bpy.data.images. Make sure it is loaded in the blend file.')

    face_obj = find_face_mesh()

    if face_obj is None:
        raise RuntimeError(f'No mesh ending with "{FACE_MESH_SUFFIX}" was found.')

    material = get_face_material(face_obj)
    image_nodes = find_face_lightmap_image_nodes(material)

    for image_node in image_nodes:
        image_node.image = image

    node_names = [node.name for node in image_nodes]

    return face_obj.name, node_names, image.name

class JIDEEH_OT_set_face_lightmap(bpy.types.Operator):
    bl_idname = "jideeh.set_face_lightmap"
    bl_label = "Set Face Lightmap"
    bl_options = {"REGISTER", "UNDO"}

    image_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        try:
            face_obj_name, node_names, image_name = set_face_lightmap_image(self.image_name)
            self.report({"INFO"}, f'Set {face_obj_name} face lightmap to {image_name}.')
            print(f'Set {face_obj_name} face lightmap to {image_name}.')
            print("Updated image texture nodes:")
            for node_name in node_names:
                print(node_name)
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_PT_face_lightmap_panel(bpy.types.Panel):
    bl_label = "Face Lightmap Switcher"
    bl_idname = "JIDEEH_PT_face_lightmap_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout

        for group_name, items in LIGHTMAP_GROUPS:
            layout.label(text=group_name)
            row = layout.row(align=True)

            for label, image_name in items:
                operator = row.operator("jideeh.set_face_lightmap", text=label)
                operator.image_name = image_name

classes = (
    JIDEEH_OT_set_face_lightmap,
    JIDEEH_PT_face_lightmap_panel,
)

def enable_register_on_this_text():
    markers = [
        "JIDEEH_PT_face_lightmap_panel",
        "jideeh.set_face_lightmap",
        "Face Lightmap Switcher",
    ]

    for text in bpy.data.texts:
        body = text.as_string()

        if all(marker in body for marker in markers):
            text.use_module = True
            return text.name

    return None

def register():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

    for cls in classes:
        bpy.utils.register_class(cls)

    enabled_text_name = enable_register_on_this_text()

    if enabled_text_name:
        print(f'Auto-register enabled for text block: {enabled_text_name}')
    else:
        print("Could not automatically find this text block to enable Register.")

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

if __name__ == "__main__":
    register()