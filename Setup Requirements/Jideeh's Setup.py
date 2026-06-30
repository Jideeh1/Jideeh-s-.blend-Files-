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
        if obj.type == "MESH" and obj.name.endswith("_Body_1"):
            body_objects_found.append(obj.name)
            modifier = obj.modifiers.get("Outlines")

            if modifier is None:
                missing_modifier_objects.append(obj.name)
            else:
                modifier.show_viewport = False
                updated_objects.append(obj.name)

    return updated_objects, missing_modifier_objects, body_objects_found

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

print("Bone collection visibility updated.")
print("Frame rate set to 24 fps.")
print("Frame range end set to 250.")
print("Render Region enabled.")
print("Resolution set to 1920 x 1080.")
print("Camera added or reused in the scene collection.")
print("Camera location, rotation, and passepartout updated.")
