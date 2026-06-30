import bpy
import math

bone_collections_off = [
    "Light Panel",
    "Facerig",
    "Main",
    "Torso (Tweak)",
    "Fingers",
    "Finger (Detail)",
    "Arm.L (IK)",
    "Arm.R (IK)",
    "Arm.L (Tweak)",
    "Arm.R (Tweak)",
    "Leg.L (FK)",
    "Leg.R (FK)",
    "Leg.L (Tweak)",
    "Leg.R (Tweak)",
    "Root",
    "Hair",
    "Clothes",
    "Misc",
]

bone_collections_on = [
    "Face",
    "Torso",
    "Arm.L (FK)",
    "Arm.R (FK)",
    "Leg.L (IK)",
    "Leg.R (IK)",
]

arm_fk_collections = [
    "Arm.L (FK)",
    "Arm.R (FK)",
]

ik_fk_property_names = [
    "IK-FK",
    "IK_FK",
    "ik_fk",
    "IK FK",
]

common_arm_property_bones = [
    "upper_arm_parent.L",
    "upper_arm_parent.R",
    "upper_arm_fk.L",
    "upper_arm_fk.R",
    "forearm_fk.L",
    "forearm_fk.R",
    "hand_fk.L",
    "hand_fk.R",
    "hand_ik.L",
    "hand_ik.R",
]

extra_fx_modifier_name = "Extra FX"
extra_fx_node_tree_name = "Extra FX Geonode"
face_shadow_input_name = "face shadow(off/on)"
combine_uv_node_name = "combine uv"
combine_uv_invert_input_name = "invert"

def normalize_name(name):
    return "".join(character.lower() for character in str(name) if character.isalnum())

def strip_blender_numeric_suffix(name):
    parts = name.rsplit(".", 1)

    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]

    return name

def is_face_mesh_object(obj):
    if obj.type != "MESH":
        return False

    base_name = strip_blender_numeric_suffix(obj.name).lower()

    return base_name.endswith("_face")

def is_body_numbered_mesh_object(obj):
    if obj.type != "MESH":
        return False

    base_name = strip_blender_numeric_suffix(obj.name).lower()

    return base_name.endswith("_body_1") or base_name.endswith("_body_2") or base_name.endswith("_body_3")

def is_body_1_mesh_object(obj):
    if obj.type != "MESH":
        return False

    base_name = strip_blender_numeric_suffix(obj.name).lower()

    return base_name.endswith("_body_1")

def is_metarig_object(obj):
    if obj.type != "ARMATURE":
        return False

    object_name = obj.name.lower()
    data_name = obj.data.name.lower() if obj.data else ""

    if object_name == "metarig" or object_name.startswith("metarig."):
        return True

    if data_name == "metarig" or data_name.startswith("metarig."):
        return True

    return False

def delete_metarig_armatures():
    deleted_objects = []

    try:
        bpy.ops.object.mode_set(mode="OBJECT")
    except Exception:
        pass

    for obj in list(bpy.data.objects):
        if is_metarig_object(obj):
            deleted_objects.append(obj.name)
            bpy.data.objects.remove(obj, do_unlink=True)

    return deleted_objects

def hide_head_direction_objects():
    hidden_objects = []

    for obj in bpy.data.objects:
        if obj.name.endswith(" Head Direction"):
            obj.hide_viewport = True
            obj.hide_set(True)
            hidden_objects.append(obj.name)

    return hidden_objects

def get_armature_object():
    obj = bpy.context.object

    if obj and obj.type == "ARMATURE" and not is_metarig_object(obj):
        return obj

    for selected_obj in bpy.context.selected_objects:
        if selected_obj.type == "ARMATURE" and not is_metarig_object(selected_obj):
            return selected_obj

    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE" and not is_metarig_object(obj):
            return obj

    for obj in bpy.data.objects:
        if obj.type == "ARMATURE" and not is_metarig_object(obj):
            return obj

    return None

def set_collection_visibility(armature, collection_names, visible, missing):
    for collection_name in collection_names:
        bone_collection = armature.collections.get(collection_name)

        if bone_collection is None:
            missing.append(collection_name)
        else:
            bone_collection.is_visible = visible

def set_ik_fk_property_on_pose_bone(pose_bone):
    updated = False

    for property_name in ik_fk_property_names:
        if property_name in pose_bone:
            pose_bone[property_name] = 1
            updated = True

    return updated

def get_pose_bones_from_collection(armature_obj, collection_name):
    armature = armature_obj.data
    bone_collection = armature.collections.get(collection_name)

    if bone_collection is None:
        return []

    pose_bones = []

    for bone in bone_collection.bones:
        pose_bone = armature_obj.pose.bones.get(bone.name)

        if pose_bone is not None:
            pose_bones.append(pose_bone)

    return pose_bones

def add_camera_to_scene_collection():
    scene = bpy.context.scene
    existing_cameras = [obj for obj in bpy.data.objects if obj.type == "CAMERA"]

    if existing_cameras:
        camera_obj = existing_cameras[0]
    else:
        camera_data = bpy.data.cameras.new("Camera")
        camera_obj = bpy.data.objects.new("Camera", camera_data)

    if scene.collection not in camera_obj.users_collection:
        scene.collection.objects.link(camera_obj)

    for collection in list(camera_obj.users_collection):
        if collection != scene.collection:
            collection.objects.unlink(camera_obj)

    camera_obj.name = "Camera"
    camera_obj.data.name = "Camera"

    camera_obj.location = (1.50661, -4.6511, 0.9646)
    camera_obj.rotation_euler = (
        math.radians(88.3172),
        math.radians(-0.000005),
        math.radians(11.6211),
    )
    camera_obj.data.passepartout_alpha = 0.85

    scene.camera = camera_obj

    return camera_obj

def disable_body_outline_modifier():
    updated_objects = []
    missing_modifier_objects = []
    body_objects_found = []

    for obj in bpy.data.objects:
        if is_body_1_mesh_object(obj):
            body_objects_found.append(obj.name)
            modifier = obj.modifiers.get("Outlines")

            if modifier is None:
                missing_modifier_objects.append(obj.name)
            else:
                modifier.show_viewport = False
                updated_objects.append(obj.name)

    return updated_objects, missing_modifier_objects, body_objects_found

def modifier_matches_extra_fx(modifier):
    if modifier.type != "NODES":
        return False

    modifier_name = normalize_name(modifier.name)
    target_modifier_name = normalize_name(extra_fx_modifier_name)

    node_group_name = ""
    target_node_group_name = normalize_name(extra_fx_node_tree_name)

    if modifier.node_group is not None:
        node_group_name = normalize_name(modifier.node_group.name)

    if target_node_group_name in node_group_name:
        return True

    if target_modifier_name in modifier_name:
        return True

    return False

def get_socket_value_for_type(socket_type):
    if socket_type in {"NodeSocketFloat", "NodeSocketFloatFactor", "NodeSocketFloatPercentage", "NodeSocketFloatDistance", "NodeSocketFloatAngle", "NodeSocketFloatTime", "NodeSocketFloatTimeAbsolute"}:
        return 1.0

    if socket_type == "NodeSocketBool":
        return True

    if socket_type in {"NodeSocketInt", "NodeSocketIntFactor", "NodeSocketIntPercentage"}:
        return 1

    return 1.0

def get_face_shadow_socket_items(node_group):
    socket_items = []
    target_name = normalize_name(face_shadow_input_name)

    if hasattr(node_group, "interface") and hasattr(node_group.interface, "items_tree"):
        for item in node_group.interface.items_tree:
            item_type = getattr(item, "item_type", None)
            item_name = getattr(item, "name", "")
            item_identifier = getattr(item, "identifier", "")
            item_in_out = getattr(item, "in_out", None)
            item_socket_type = getattr(item, "socket_type", "")

            if item_type == "SOCKET" and item_identifier:
                if item_in_out in {None, "INPUT"}:
                    if normalize_name(item_name) == target_name:
                        socket_items.append((item_identifier, item_name, item_socket_type))

    if socket_items:
        return socket_items

    if hasattr(node_group, "inputs"):
        for socket in node_group.inputs:
            socket_name = getattr(socket, "name", "")
            socket_identifier = getattr(socket, "identifier", "")
            socket_type = getattr(socket, "bl_socket_idname", "")

            if socket_identifier and normalize_name(socket_name) == target_name:
                socket_items.append((socket_identifier, socket_name, socket_type))

    return socket_items

def set_face_shadow_on_modifier(modifier):
    if modifier.node_group is None:
        return False, []

    updated = []
    socket_items = get_face_shadow_socket_items(modifier.node_group)

    for identifier, socket_name, socket_type in socket_items:
        value = get_socket_value_for_type(socket_type)

        try:
            modifier[identifier] = value
            updated.append(f"{identifier} = {value}")
        except Exception as error:
            print(f"Could not set {socket_name} using {identifier}: {error}")

        try:
            modifier[f"{identifier}_use_attribute"] = False
        except Exception:
            pass

    try:
        modifier.id_data.update_tag()
    except Exception:
        pass

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    return len(updated) > 0, updated

def print_modifier_debug_info(obj, modifier):
    print("Debug info for Geometry Nodes modifier:")
    print(obj.name)
    print(modifier.name)

    if modifier.node_group is not None:
        print("Node tree:")
        print(modifier.node_group.name)

    print("Modifier custom keys:")
    for key in modifier.keys():
        try:
            print(f"{key} = {modifier[key]}")
        except Exception:
            print(key)

    if modifier.node_group is not None and hasattr(modifier.node_group, "interface") and hasattr(modifier.node_group.interface, "items_tree"):
        print("Node group interface sockets:")
        for item in modifier.node_group.interface.items_tree:
            item_type = getattr(item, "item_type", None)
            item_name = getattr(item, "name", "")
            item_identifier = getattr(item, "identifier", "")
            item_in_out = getattr(item, "in_out", None)
            item_socket_type = getattr(item, "socket_type", None)

            if item_type == "SOCKET":
                print(f"{item_name} | {item_identifier} | {item_in_out} | {item_socket_type}")

    if modifier.node_group is not None and hasattr(modifier.node_group, "inputs"):
        print("Node group inputs:")
        for index, socket in enumerate(modifier.node_group.inputs):
            socket_name = getattr(socket, "name", "")
            socket_identifier = getattr(socket, "identifier", "")
            socket_type = getattr(socket, "bl_socket_idname", "")
            print(f"{index} | {socket_name} | {socket_identifier} | {socket_type}")

def enable_face_shadow_extra_fx():
    face_objects_found = []
    matching_modifiers_found = []
    updated_face_shadow = []
    missing_modifier_objects = []
    missing_input_modifiers = []

    for obj in bpy.data.objects:
        if is_face_mesh_object(obj):
            face_objects_found.append(obj.name)
            matching_modifiers = []

            for modifier in obj.modifiers:
                if modifier_matches_extra_fx(modifier):
                    matching_modifiers.append(modifier)

            if not matching_modifiers:
                missing_modifier_objects.append(obj.name)

            for modifier in matching_modifiers:
                matching_modifiers_found.append(f"{obj.name} -> {modifier.name}")
                updated, updates = set_face_shadow_on_modifier(modifier)

                if updated:
                    updated_face_shadow.append(f"{obj.name} -> {modifier.name} -> {', '.join(updates)}")
                else:
                    missing_input_modifiers.append(f"{obj.name} -> {modifier.name}")
                    print_modifier_debug_info(obj, modifier)

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    return face_objects_found, matching_modifiers_found, updated_face_shadow, missing_modifier_objects, missing_input_modifiers

def node_matches_combine_uv(node):
    target_name = normalize_name(combine_uv_node_name)
    node_name = normalize_name(getattr(node, "name", ""))
    node_label = normalize_name(getattr(node, "label", ""))
    node_tree_name = ""

    if hasattr(node, "node_tree") and node.node_tree is not None:
        node_tree_name = normalize_name(node.node_tree.name)

    if target_name in node_name:
        return True

    if target_name in node_label:
        return True

    if target_name in node_tree_name:
        return True

    return False

def input_matches_invert(socket):
    target_name = normalize_name(combine_uv_invert_input_name)
    socket_name = normalize_name(getattr(socket, "name", ""))

    if socket_name == target_name:
        return True

    if target_name in socket_name:
        return True

    return False

def set_socket_default_to_zero(socket):
    if not hasattr(socket, "default_value"):
        return False

    try:
        current_value = socket.default_value
    except Exception:
        return False

    try:
        if isinstance(current_value, bool):
            socket.default_value = False
        elif isinstance(current_value, int):
            socket.default_value = 0
        elif isinstance(current_value, float):
            socket.default_value = 0.0
        else:
            socket.default_value = 0.0

        return True
    except Exception:
        return False

def print_material_node_debug_info(obj, material):
    print("Debug info for body material nodes:")
    print(obj.name)
    print(material.name)

    if material.node_tree is None:
        print("No material node tree.")
        return

    for node in material.node_tree.nodes:
        node_tree_name = ""

        if hasattr(node, "node_tree") and node.node_tree is not None:
            node_tree_name = node.node_tree.name

        print(f"Node: {node.name} | Label: {node.label} | Type: {node.bl_idname} | Node Tree: {node_tree_name}")

        for socket in node.inputs:
            if hasattr(socket, "default_value"):
                try:
                    print(f"Input: {socket.name} = {socket.default_value}")
                except Exception:
                    print(f"Input: {socket.name}")

def set_combine_uv_invert_in_node_tree(node_tree, material_name, visited_node_trees):
    updated = []
    missing_invert_nodes = []
    combine_uv_nodes_found = []

    if node_tree is None:
        return updated, missing_invert_nodes, combine_uv_nodes_found

    if node_tree.name in visited_node_trees:
        return updated, missing_invert_nodes, combine_uv_nodes_found

    visited_node_trees.add(node_tree.name)

    for node in node_tree.nodes:
        if node_matches_combine_uv(node):
            node_tree_name = ""

            if hasattr(node, "node_tree") and node.node_tree is not None:
                node_tree_name = node.node_tree.name

            combine_uv_nodes_found.append(f"{material_name} -> {node.name} -> {node_tree_name}")
            invert_socket_found = False

            for socket in node.inputs:
                if input_matches_invert(socket):
                    invert_socket_found = True

                    if set_socket_default_to_zero(socket):
                        updated.append(f"{material_name} -> {node.name} -> {socket.name} = 0")
                    else:
                        missing_invert_nodes.append(f"{material_name} -> {node.name} -> {socket.name}")

            if not invert_socket_found:
                missing_invert_nodes.append(f"{material_name} -> {node.name}")

        if hasattr(node, "node_tree") and node.node_tree is not None:
            nested_updated, nested_missing, nested_found = set_combine_uv_invert_in_node_tree(node.node_tree, material_name, visited_node_trees)
            updated.extend(nested_updated)
            missing_invert_nodes.extend(nested_missing)
            combine_uv_nodes_found.extend(nested_found)

    try:
        node_tree.update_tag()
    except Exception:
        pass

    return updated, missing_invert_nodes, combine_uv_nodes_found

def set_body_material_combine_uv_invert_to_zero():
    body_objects_found = []
    materials_checked = []
    updated_invert_sockets = []
    combine_uv_nodes_found = []
    missing_material_objects = []
    missing_node_materials = []
    missing_invert_inputs = []

    for obj in bpy.data.objects:
        if is_body_numbered_mesh_object(obj):
            body_objects_found.append(obj.name)
            object_materials = []

            for material_slot in obj.material_slots:
                material = material_slot.material

                if material is not None:
                    object_materials.append(material)

            object_materials = list(dict.fromkeys(object_materials))

            if not object_materials:
                missing_material_objects.append(obj.name)

            for material in object_materials:
                materials_checked.append(f"{obj.name} -> {material.name}")

                if not material.use_nodes or material.node_tree is None:
                    missing_node_materials.append(f"{obj.name} -> {material.name}")
                    continue

                updated, missing_invert, found_nodes = set_combine_uv_invert_in_node_tree(material.node_tree, material.name, set())

                if updated:
                    for update in updated:
                        updated_invert_sockets.append(f"{obj.name} -> {update}")

                if found_nodes:
                    for found_node in found_nodes:
                        combine_uv_nodes_found.append(f"{obj.name} -> {found_node}")
                else:
                    missing_node_materials.append(f"{obj.name} -> {material.name}")
                    print_material_node_debug_info(obj, material)

                if missing_invert:
                    for missing in missing_invert:
                        missing_invert_inputs.append(f"{obj.name} -> {missing}")

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    return body_objects_found, materials_checked, combine_uv_nodes_found, updated_invert_sockets, missing_material_objects, missing_node_materials, missing_invert_inputs

deleted_metarigs = delete_metarig_armatures()
hidden_head_direction_objects = hide_head_direction_objects()

armature_obj = get_armature_object()

if armature_obj is None:
    raise RuntimeError("No non-metarig armature object was found in the scene or file.")

try:
    bpy.ops.object.mode_set(mode="OBJECT")
except Exception:
    pass

bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = armature_obj
armature_obj.select_set(True)

scene = bpy.context.scene
scene.render.fps = 24
scene.frame_end = 250
scene.render.use_border = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

camera_obj = add_camera_to_scene_collection()

outline_updated_objects, outline_missing_modifier_objects, body_objects_found = disable_body_outline_modifier()
face_objects_found, extra_fx_modifiers_found, face_shadow_updated_modifiers, face_missing_modifier_objects, face_missing_input_modifiers = enable_face_shadow_extra_fx()
body_material_objects_found, body_materials_checked, combine_uv_nodes_found, combine_uv_invert_updated, body_missing_material_objects, body_missing_node_materials, combine_uv_missing_invert_inputs = set_body_material_combine_uv_invert_to_zero()

armature = armature_obj.data
missing_collections = []
updated_ik_fk_bones = []

set_collection_visibility(armature, bone_collections_off, False, missing_collections)
set_collection_visibility(armature, bone_collections_on, True, missing_collections)

for collection_name in arm_fk_collections:
    for pose_bone in get_pose_bones_from_collection(armature_obj, collection_name):
        if set_ik_fk_property_on_pose_bone(pose_bone):
            updated_ik_fk_bones.append(pose_bone.name)

for bone_name in common_arm_property_bones:
    pose_bone = armature_obj.pose.bones.get(bone_name)

    if pose_bone is not None:
        if set_ik_fk_property_on_pose_bone(pose_bone):
            updated_ik_fk_bones.append(pose_bone.name)

for pose_bone in armature_obj.pose.bones:
    if pose_bone.name.endswith(".L") or pose_bone.name.endswith(".R"):
        if "arm" in pose_bone.name.lower() or "hand" in pose_bone.name.lower() or "forearm" in pose_bone.name.lower():
            if set_ik_fk_property_on_pose_bone(pose_bone):
                updated_ik_fk_bones.append(pose_bone.name)

updated_ik_fk_bones = list(dict.fromkeys(updated_ik_fk_bones))

print("Using armature:")
print(armature_obj.name)

if deleted_metarigs:
    print("Deleted metarig armatures:")
    for object_name in deleted_metarigs:
        print(object_name)
else:
    print("No metarig armatures found.")

if hidden_head_direction_objects:
    print("Head Direction objects hidden in viewport:")
    for object_name in hidden_head_direction_objects:
        print(object_name)
else:
    print("No Head Direction objects found.")

if missing_collections:
    print("These bone collections were not found:")
    for collection_name in missing_collections:
        print(collection_name)

if updated_ik_fk_bones:
    print("IK-FK was set to 1 on these bones:")
    for bone_name in updated_ik_fk_bones:
        print(bone_name)
else:
    print("No IK-FK custom property was found on the arm FK collections or common arm property bones.")

if body_objects_found:
    print("_Body_1 mesh objects found:")
    for object_name in body_objects_found:
        print(object_name)
else:
    print("No mesh ending with _Body_1 was found.")

if outline_updated_objects:
    print("Outlines modifier viewport display disabled on:")
    for object_name in outline_updated_objects:
        print(object_name)
else:
    print("No Outlines modifier viewport display was disabled.")

if outline_missing_modifier_objects:
    print("These _Body_1 meshes did not have an Outlines modifier:")
    for object_name in outline_missing_modifier_objects:
        print(object_name)

if face_objects_found:
    print("_face or _Face mesh objects found:")
    for object_name in face_objects_found:
        print(object_name)
else:
    print("No mesh ending with _face or _Face was found.")

if extra_fx_modifiers_found:
    print("Extra FX Geonode modifiers found:")
    for modifier_name in extra_fx_modifiers_found:
        print(modifier_name)
else:
    print("No matching Extra FX Geonode modifier was found on any _face or _Face mesh.")

if face_shadow_updated_modifiers:
    print("face shadow(off/on) was set on:")
    for modifier_name in face_shadow_updated_modifiers:
        print(modifier_name)
else:
    print("face shadow(off/on) was not updated on any matching Extra FX Geonode modifier.")

if face_missing_modifier_objects:
    print("These _face or _Face meshes did not have the matching Extra FX Geonode modifier:")
    for object_name in face_missing_modifier_objects:
        print(object_name)

if face_missing_input_modifiers:
    print("These matching Extra FX Geonode modifiers did not expose a face shadow(off/on) input:")
    for modifier_name in face_missing_input_modifiers:
        print(modifier_name)

if body_material_objects_found:
    print("_Body_1, _Body_2, or _Body_3 mesh objects found for material Combine UV update:")
    for object_name in body_material_objects_found:
        print(object_name)
else:
    print("No mesh ending with _Body_1, _Body_2, or _Body_3 was found for material Combine UV update.")

if body_materials_checked:
    print("Materials checked on body meshes:")
    for material_name in body_materials_checked:
        print(material_name)

if combine_uv_nodes_found:
    print("Combine UV nodes found:")
    for node_name in combine_uv_nodes_found:
        print(node_name)
else:
    print("No Combine UV nodes were found on _Body_1, _Body_2, or _Body_3 materials.")

if combine_uv_invert_updated:
    print("Combine UV invert sliders set to 0:")
    for update in combine_uv_invert_updated:
        print(update)
else:
    print("No Combine UV invert slider was updated.")

if body_missing_material_objects:
    print("These body meshes did not have materials:")
    for object_name in body_missing_material_objects:
        print(object_name)

if body_missing_node_materials:
    print("These body mesh materials did not have node trees or did not contain a Combine UV node:")
    for material_name in body_missing_node_materials:
        print(material_name)

if combine_uv_missing_invert_inputs:
    print("These Combine UV nodes did not expose an invert input or could not be updated:")
    for node_name in combine_uv_missing_invert_inputs:
        print(node_name)

print("Bone collection visibility updated.")
print("Frame rate set to 24 fps.")
print("Frame range end set to 250.")
print("Render Region enabled.")
print("Resolution set to 1920 x 1080.")
print("Camera added or reused in the scene collection.")
print("Camera location, rotation, and passepartout updated.")
print("Body material Combine UV invert sliders updated.")