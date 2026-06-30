### CREDITS:
### Rigging+Scripting: Enthralpy
### Shader: Just_ScaasI, BonnyAnimations, Aiko
### Supervised and made possible by Stormz67  

# INSTRUCTION
# Import using betterfbx
# Run this script
# Long chains of bones like tails usually have broken parenting. Select the tail bones and then run script #2

import bpy
ver = bpy.app.version_string
if ver[:3] == '4.0':
    ver = 4
elif ver[0] == '4':
    ver = float(ver[:3])
elif ver[0] == '3':
    ver = 3
else:
    raise Exception("youre using blender 3 or blender 4 right??")

# Use BetterFBX to load in the FBX of your ZZZ model.  Run this script and uh hopefully it works lmao. Also remember to change charname to the character's name.

charname = None

# If you want to manually rename the character (Some character names arent their actual ingame names), remove the hashtag in the next line and replace 'Burnice'
#charname = "Burnice "


def findpath():
    for img in bpy.data.images:
        if "_map" in img.name.lower() or "d.png" in img.name.lower():
            path = img.filepath.replace("\\","/")
            break
    splits = path.split("/")
#    if splits[-2] == "Textures":
#        newpath = "/".join(splits[0:-1])
#    else: # no Textures folder, imgs are in same folder as the fbx
#        newpath = "/".join(splits[0:-2])

    newpath = "/".join(splits[0:-1])  ## top 4 lines prove I'm a dumbass.
    return newpath.replace("\\", "/")

folder = findpath()
folder = bpy.path.abspath(folder)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.scale_clear(clear_delta=False)
bpy.ops.object.select_all(action='DESELECT')
 
# Thank you 2.3 for making this necessary, goddamn. 
for obj in bpy.data.objects:
    screwyou = bpy.data.objects.get("Bone_Root")
    if screwyou and screwyou.type == 'ARMATURE':
        for obj in bpy.data.objects:
            if obj.name.lower().endswith("yidhari_eyebrow"):
                obj.parent = screwyou
                obj.rotation_quaternion = (1,0,0,0)

for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' and obj.name == "Bone_Root": # Usually the rig doesnt have an Empty as a parent. If it does, the rig name is fucked, need to fix.
            obj.parent.name += "A"
            obj.name = obj.parent.name[:-1]
            obj.data.name = obj.name # Armature data name and armature object name need to match            
            bpy.data.objects.remove(obj.parent, do_unlink=True) # Delete the parent
            obj.rotation_quaternion = (1,0,0,0) # Reset the rotation 

    #fuckyou orphie, this is to fix orphie weird bone swap
    A=bpy.context.object
    if A and A.type=='ARMATURE' and A.name=="Avatar_Female_Size02_Brujas_UI":
        b=[("Bip001 R Toe0","Skn_R_Shoelace_New_03"),
        ("Bip001 L Toe0","Skn_L_Shoelace_New_03"),
        ("Bip001 R Foot","Skn_R_Shoelace_New_01"),
        ("Bip001 L Foot","Skn_L_Shoelace_New_01")]
        bpy.ops.object.mode_set(mode='EDIT')
        for a,c in b:
            x,y=A.data.edit_bones.get(a),A.data.edit_bones.get(c)
            if x and y:x.name="TMP";y.name=a;A.data.edit_bones["TMP"].name=c 

for obj in bpy.data.objects:
    if "_face" in obj.name.lower() and "weapon_" not in obj.name.lower() and "gun_" not in obj.name.lower(): # gdi orphie
        faceobj = obj
    if obj.type == 'ARMATURE' and 'Lighting' not in obj.name and 'Eye' not in obj.name:
        arm = obj
        if charname is None: # If youre not manually renaming.
            charname = arm.name.split("_")[-1] + " "
            if charname == "UI ":
                charname = arm.name.split("_")[-2] + " "
            if charname == "Model ":
                charname = arm.name.split("_")[-2] + " "
                
    if "HairShadow" in obj.name:
#        bpy.data.objects.remove(obj, do_unlink=True)
        obj.hide_viewport = True
        obj.hide_render = True
    if "FX" in obj.name:
        obj.hide_viewport = True
        obj.hide_render = True
    if obj.type == 'EMPTY' and "Head " not in obj.name and "Light " not in obj.name and obj.users_collection[0].name != "LP wgt" and obj.parent != bpy.data.objects["Lighting Panel"]:
        bpy.data.objects.remove(obj, do_unlink=True) # this only works for empties; otherwise youd have to also delete object data, which empties dont have
arm.show_in_front = True



################################### SHADER SECTION ###############################

print("\n\ntEST")
###### FIX EYE SHADOW ###### 
def fixeyeshadow():
    bpy.context.view_layer.objects.active = faceobj
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = faceobj
    faceobj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    
    matlen = len(faceobj.material_slots)
#    if matlen == 2:
    count = 0
    for obj in bpy.data.objects:
        if "NPC" in obj.name:
            return
    for mat in faceobj.material_slots:
        if "_eye" in mat.name.lower() and "brows" not in mat.name.lower():
            faceobj.active_material_index = count
        if "_Ben_" in mat.name or "PanYinhu" in mat.name: ### OR YINHU
            return
        count += 1
#    faceobj.active_material_index = 1
    bpy.ops.object.material_slot_select() # Select all verts in eye mat

    # deselect Eye_R and Eye_L verts.  why are there like 3 diff eye names.
    
    for vg in ['Eye_R','Skn_R_Eye','Skn_R_Pupil','Bdy_R_Eye', 'Skn_Bn_Eye_R', 'Bn_Eye_R', 'Skn_R_Highlights', 'EYE_R']:
        try:
            bpy.ops.object.vertex_group_set_active(group=vg)
            bpy.ops.object.vertex_group_deselect()  # Putting this here bc new models have Highhlights VG with eye VG
        except:
            pass

    for vg in ['Eye_L','Skn_L_Eye','Skn_L_Pupil','Bdy_L_Eye', 'Skn_Bn_Eye_L', 'Bn_Eye_L', 'Skn_L_Highlights', 'EYE_L']:
        try:
            bpy.ops.object.vertex_group_set_active(group=vg)
            bpy.ops.object.vertex_group_deselect()
        except:
            pass             
    
    
    bpy.ops.object.vertex_group_deselect()
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.object.material_slot_add()
    bpy.context.object.material_slots[-1].material = bpy.data.materials["Eye Transparent"]
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all( action = 'DESELECT' )
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
import os
### SCAN FOR IMAGES ###
def scan(folder):
    dick = {}
    bodyparts = ["Body_1", "Body_2", "Face", "Weapon", "Weapon_2", "Hair", "Leg", "Body_3", "Tail"]
    ### Note: Body_Map1, Body_Map2, Weapon_A, Weapon_2_A. annoying af.        
    for body in bodyparts:
        dick[body] = []
        
    for obj in bpy.data.objects: #to fix ye shunguang hair anomaly
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                if slot.material and slot.material.name == "MAT_Zhenzhen_Hair_T_UI":
                    slot.material = bpy.data.materials.get("MAT_Zhenzhen_Hair_UI")
        
    for filename in os.listdir(folder): # goddamn wtf is up with these two characters
        if "Astra_Chandelier_Map1_D" in filename:
            bpy.data.images["Astra_Chandelier_Map1_D.png"].name = "Astra_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Chandelier", "Body")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Astra_Chandelier" in filename:
            replacement = folder + "/" + filename.replace("Chandelier", "Body")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        if "Norano_WhiteHeart_Map1_D" in filename:
            bpy.data.images["Norano_WhiteHeart_Map1_D.png"].name = "Norano_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map1_D", "Norano_Body_Map1_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
        elif "Norano_WhiteHeart_Map2_D" in filename:
            bpy.data.images["Norano_WhiteHeart_Map2_D.png"].name = "Norano_Body_Map2_D.png"
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map2_D", "Norano_Body_Map2_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Norano_WhiteHeart" in filename:
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map", "Norano_Body_Map")
            filename = folder + "/" + filename
            os.rename(filename, replacement)

        if "Clara_Map1_D" in filename:
            bpy.data.images["Clara_Map1_D.png"].name = "Clara_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Clara_Map1_D", "Clara_Body_Map1_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
        elif "Clara_Map2_D" in filename:
            bpy.data.images["Clara_Map2_D.png"].name = "Clara_Body_Map2_D.png"
            replacement = folder + "/" + filename.replace("Clara_Map2_D", "Clara_Body_Map2_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Clara_Map" in filename:
            replacement = folder + "/" + filename.replace("Clara_Map", "Clara_Body_Map")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        if "Alice_Swimwear_Weanpon" in filename:
            bpy.data.images["Alice_Swimwear_Weanpon_Map1_D.png"].name = "Alice_Swimwear_Weapon_Map1_D.png"
            replacement = folder + "/" + filename.replace("Alice_Swimwear_Weanpon", "Alice_Swimwear_Weapon")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
    for img in bpy.data.images: #to fix the setup for the 2nd time
        if "Chandelier" in img.name:
            new_name = img.name.replace("Chandelier", "Body")
            img.name = new_name
            img.filepath = folder + "/" + "Astra_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Clara_Map1_D.png" in img.name:
            bpy.data.images["Clara_Map1_D.png"].name = "Clara_Body_Map1_D.png"
            img.filepath = folder + "/" + "Clara_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Clara_Map2_D.png" in img.name:
            bpy.data.images["Clara_Map2_D.png"].name = "Clara_Body_Map2_D.png"
            img.filepath = folder + "/" + "Clara_Body_Map2_D.png"
            img.reload()
            replaced = True
        if "Norano_WhiteHeart_Map1_D.png" in img.name:
            bpy.data.images["Norano_WhiteHeart_Map1_D.png"].name = "Norano_Body_Map1_D.png"
            img.filepath = folder + "/" + "Norano_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Norano_WhiteHeart_Map2_D.png" in img.name:
            bpy.data.images["Norano_WhiteHeart_Map2_D.png"].name = "Norano_Body_Map2_D.png"
            img.filepath = folder + "/" + "Norano_Body_Map2_D.png"
            img.reload()
            replaced = True
        if "Alice_Swimwear_Weanpon_Map1_D.png" in img.name:
            new_name = img.name.replace("Alice_Swimwear_Weanpon_Map1_D.png", "Alice_Swimwear_Weapon_Map1_D.png")
            img.name = new_name
            img.filepath = folder + "/" + "Alice_Swimwear_Weapon_Map1_D.png"
            img.reload()
            replaced = True
                    
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if (filename[-15:-10] + filename[-7:-6]) == "Body_1" or (filename[-10:-5] + filename[-4:]) == "Body_.png" or (filename[-12:-5] + filename[-4:]) == "Body_1_.png": 
            dick["Body_1"].append(filename)
        elif (filename[-15:-10] + filename[-7:-6]) == "Body_2" or (filename[-12:-5] + filename[-4:]) == "Body_2_.png":
            dick["Body_2"].append(filename)
        elif "Weapon_2" in filename:
            dick["Weapon_2"].append(filename)
        elif "weapon" in filename.lower():
            dick["Weapon"].append(filename)
        elif "Face" in filename:
            dick["Face"].append(filename)
        elif "Hair" in filename:
            dick["Hair"].append(filename)
        elif "Leg" in filename:
            dick["Leg"].append(filename)  
        elif "Tail" in filename:
            dick["Tail"].append(filename)    
        elif (filename[-15:-10] + filename[-7:-6]) == "Body_3" or (filename[-12:-5] + filename[-4:]) == "Body_3_.png":
            dick["Body_3"].append(filename)    
            print("A\n\n")
    for k in dick:
        print(k, dick[k])
            
    return dick
        
def assignmats(mats, outs):
    for mat in bpy.data.materials:
        if "Outlines" in mat.name:
            outs.append(mat)
        elif "Shader" in mat.name:
            mats.append(mat)
            
def assignshader(arm):
    body2 = False
    for obj in arm.children:
        if "Body_2" in obj.name and "NuoCha" not in obj.name: # gfdi nicole
            body2 = True
        
            
    for obj in arm.children:
        mats = obj.data.materials
        for x in range(0, len(obj.data.materials)):
            mat = mats[x]
            if "Body_1" in mat.name or "Clara_Map1" in mat.name or (body2 == False and "Body" in mat.name and "_2" not in mat.name):
                mats[x] = bpy.data.materials["ZZZ Shader Body"]
                imgnode(mats[x], "Body_1")
    
            elif "Body_2" in mat.name or "Clara_Map2" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body 2"]
                imgnode(mats[x], "Body_2")
                
            elif "Hair_T_" in mat.name or mat.name.endswith("Hair_T"): # this bitch can be either body_1 or body_2 or smthng
                imgname = mat.node_tree.nodes["Image Texture"].image.name
                checks = ["body_map1", "body_d", "body_1_d"]
                body1 = False
                for check in checks:
                    if check in imgname.lower():
                        mats[x] = bpy.data.materials["ZZZ Shader Body"]
                        imgnode(mats[x], "Body_1")
                        body1 = True
                        break
                if not body1:
                    mats[x] = bpy.data.materials["ZZZ Shader Body 2"]
                    imgnode(mats[x], "Body_2")
            
            elif "Body_3" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"]
                imgnode(mats[x], "Body_3")
                
            elif "Face" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Face"]
                imgnode(mats[x], "Face")
            elif "Eye" in mat.name and mat.name != "Eye Transparent":
#                mats[x] = bpy.data.materials["ZZZ Shader Eye"]
                mats[x] = bpy.data.materials["ZZZ Shader Face"]
                imgnode(mats[x], "Face")
                
            elif "Hair" in mat.name and "Shadow" not in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Hair"]
                imgnode(mats[x], "Hair")
                
            elif "Leg" in mat.name and "Shadow" not in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"]
                imgnode(mats[x], "Leg")    
            elif "Tail" in mat.name: # I hope no character ever has tail, leg, and body3 all at once lmao.
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"] 
                imgnode(mats[x], "Tail")    
                
            elif "Weapon_" in mat.name or "_Weapon" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Weapon"]
                imgnode(mats[x], "Weapon")
            elif "Weapon_2" in mat.name: # Mat names are Weapon_ and Weapon_2
                try:
                    mats[x] = bpy.data.materials["ZZZ Shader Weapon 2"]
                except:
                    newmat = bpy.data.materials["ZZZ Shader Weapon"]
                    mats[x] = newmat.copy()
                    mats[x].name = "ZZZ Shader Weapon 2"
                imgnode(mats[x], "Weapon_2")
                
def imgnode(mat, name):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            type = node.name[-1] + ".png" # D.png, A.png, etc
            for f in files[name]:
                if f.endswith("D.png") and node.name.endswith("_D"): # dumbass u forgot this already gets imported
                    node.image = bpy.data.images[f]
                    node.image.alpha_mode = 'CHANNEL_PACKED'
#                    print(mat.name, name, node.image)

                elif f.endswith(type):
                    img = bpy.data.images.load(folder + "/" + f)
                    node.image = img
                    node.image.colorspace_settings.name = 'Non-Color'
                    node.image.alpha_mode = 'CHANNEL_PACKED'
                    
                elif "face" in f.lower() and "lightmap" in f.lower(): # face lightmap
                    lnode = bpy.data.node_groups["Face Lightmap"].nodes["Face_Lightmap"]
                    img = bpy.data.images.load(folder + "/" + f)
                    lnode.image = img
                    lnode.image.colorspace_settings.name = 'Non-Color'
                    lnode.image.alpha_mode = 'CHANNEL_PACKED'
#            print(node.name, node.image.name, sep=": ")
#                    pass
            
    
files = scan(folder)

def addlightvec():
    for obj in arm.children:
        mod = obj.modifiers.new(type="NODES",name="Light Vectors")
        mod.node_group = bpy.data.node_groups["Light Vectors"]
        mod["Input_3"] = bpy.data.objects["Light Direction"]
        mod["Input_4"] = bpy.data.objects["Head Direction"]
        mod["Input_5"] = bpy.data.objects["Head Forward"]
        mod["Input_6"] = bpy.data.objects["Head Up"]
        
        obs = bpy.data.objects
        mod["Socket_0"] = obs["ColorWheel-Ambient"]
        mod["Socket_1"] = obs["ColorPicker-Ambient"]
        mod["Socket_2"] = obs["ColorWheel-Lit"]
        mod["Socket_3"] = obs["ColorPicker-Lit"]
        mod["Socket_4"] = obs["ColorWheel-Shadow"]
        mod["Socket_5"] = obs["ColorPicker-Shadow"]
        mod["Socket_6"] = obs["ColorWheel-RimLit"]
        mod["Socket_7"] = obs["ColorPicker-RimLit"]
        mod["Socket_8"] = obs["ColorWheel-RimShadow"]
        mod["Socket_9"] = obs["ColorPicker-RimShadow"]
        mod["Socket_26"] = obs["Origin-RimX"]
        mod["Socket_27"] = obs["Slider-RimX"]
        mod["Socket_28"] = obs["Origin-RimY"]
        mod["Socket_29"] = obs["Slider-RimY"]

fixeyeshadow()
mats = []
outs = []
assignmats(mats, outs)
assignshader(arm)
addlightvec()


#################################### GEONODE SECTION ###############################


def add_driver(source, target, path, dataPath):
    d = source.driver_add( path).driver
    v = d.variables.new()
    d.type = "AVERAGE"
    v.name                 = "Input_7"
    v.targets[0].id        = target
    v.targets[0].data_path = dataPath
    
def modassign(mod):
        mod['Input_3_use_attribute'] = 0
        mod["Input_12"] = True
        mod["Input_13"] = True
        mod["Input_10"] = bpy.data.materials["ZZZ Shader Hair"]
        mod["Input_5"] = bpy.data.materials["ZZZ Hair Outlines"]
        mod["Input_11"] = bpy.data.materials["ZZZ Shader Body"]
        mod["Input_9"] = bpy.data.materials["ZZZ Body Outlines"]
        mod["Input_14"] = bpy.data.materials["ZZZ Shader Body 2"]
        mod["Input_15"] = bpy.data.materials["ZZZ Body 2 Outlines"]
        mod["Input_18"] = bpy.data.materials["ZZZ Shader Body"]
        mod["Input_19"] = bpy.data.materials["ZZZ Body Outlines"]
        mod["Input_24"] = bpy.data.materials["ZZZ Shader Weapon"]
        mod["Input_25"] = bpy.data.materials["ZZZ Weapon Outlines"]
        mod["Input_26"] = bpy.data.materials["ZZZ Shader Weapon"]
        mod["Input_27"] = bpy.data.materials["ZZZ Weapon Outlines"]
        mod["Socket_0"] = bpy.data.materials["ZZZ Shader Body3/Leg"]
        mod["Socket_1"] = bpy.data.materials["ZZZ Body3/Leg Outlines"]

def syncdriver(source, name, target, path): # Make drivers for cast shadow values to sync them across bodyparts
    d = source.driver_add(path).driver
    v = d.variables.new()
    d.type = "AVERAGE"
    v.name                 = name
    v.targets[0].id        = target
    v.targets[0].data_path = path
    
        

def geonode(arm):
    inputs = ["Input_10" , "Input_5" , "Input_11" , "Input_9" , "Input_14" , "Input_15" , "Input_18" , "Input_19" , "Input_24" , "Input_25" , "Input_26" , "Input_27", "Socket_0", "Socket_1"]
    grp = bpy.data.node_groups["ZZZ Outlines"]
    for obj in arm.children: # This is for finding the main body object to do driver stuff
        if "body_1" in obj.name.lower() or obj.name[-5:].lower() == "_body" or obj.name.endswith("Body1"):
            mod = obj.modifiers.new("Extra FX", "NODES")
            mod.node_group = bpy.data.node_groups["Extra FX Geonode"] # Assign extra fx geonode
            mod["Socket_0_attribute_name"] = "cast shadow" # order matters; fx geonode needs to be above outline.
            mod["Socket_11_attribute_name"] = "shadowsharpness"   

            bod = obj
            mod = obj.modifiers.new("Outlines", "NODES")
            mod.node_group = grp
            modassign(mod)
            break
        
    for ob in arm.children: # Assign outlines modifier to other meshes
        if "body_1" in ob.name.lower() or ob.name[-5:].lower() == "_body":
            pass # already did this. 
        else:
            mod = ob.modifiers.new("Extra FX", "NODES")
            mod.node_group = bpy.data.node_groups["Extra FX Geonode"] # Assign extra fx geonode
            mod["Socket_0_attribute_name"] = "cast shadow"
            mod["Socket_11_attribute_name"] = "shadowsharpness"   
#            mod["Output_3_attribute_name"] = "depth"
#            mod["Output_2_attribute_name"] = "blend"         

            if ob == obj: # ignore this body obj, already assigned
                continue
            if "face" in ob.name.lower(): ### Only face needs these geonode attributes
                mod["Output_3_attribute_name"] = "depth"
                mod["Output_2_attribute_name"] = "blend"
                mod["Socket_5_attribute_name"] = "face shadow"
                mod["Socket_6_attribute_name"] = "faceshadX"
                mod["Socket_7_attribute_name"] = "faceshadY"
                mod["Socket_9_attribute_name"] = "faceshadadjust"

                continue # Skip adding outline geonode to face; do it with Solidify manually.
            mod = ob.modifiers.new("Outlines", "NODES")
            mod.node_group = grp
            modassign(mod)
            add_driver(ob, bod, 'modifiers["Outlines"]["Input_7"]', 'modifiers["Outlines"]["Input_7"]')
            
    for ob in arm.children: # Cast shadow driver
        if ob == faceobj:
            pass
        else:
            syncdriver(ob, "Socket_1", faceobj, 'modifiers["Extra FX"]["Socket_1"]') # cast shadow
            syncdriver(ob, "Socket_10", faceobj, 'modifiers["Extra FX"]["Socket_10"]') # shadow sharpness
        
        
def findimg(name):
    for img in bpy.data.images:
        if img.name.endswith(name):
            return img
        
def outlineshader():
    mat = bpy.data.materials["ZZZ Body Outlines"]
    for mat in bpy.data.materials:
        if "Outlines" in mat.name: 
            nodes = mat.node_tree.nodes
            if "Body 2 Outlines" in mat.name and bpy.data.materials["ZZZ Shader Body 2"].node_tree.nodes["Body_D"].image != None: # Make sure body2 actually exists since youre checking every material
                nodes["Outline_Diffuse"].image = findimg("Body_Map2_D.png")
                nodes["Outline_Lightmap"].image = findimg("Body_Map2_M.png")
                
                if nodes["Outline_Diffuse"].image == None:
                    nodes["Outline_Diffuse"].image = findimg("Body_2_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Body_2_M.png")
                    
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Body3/Leg Outlines" in mat.name and bpy.data.materials["ZZZ Shader Body3/Leg"].node_tree.nodes["Body_D"].image != None:
                nodes["Outline_Diffuse"].image = findimg("Body_Map3_D.png")
                nodes["Outline_Lightmap"].image = findimg("Body_Map3_M.png")
                
                if nodes["Outline_Diffuse"].image == None: # schoolEllen and hugo dont have 'map' in the name wtf.
                    nodes["Outline_Diffuse"].image = findimg("Body_3_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Body_3_M.png")
                
                if nodes["Outline_Diffuse"].image == None: # this means it's leg, not body3.
                    nodes["Outline_Diffuse"].image = findimg("Leg_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Leg_M.png")
                    
                if nodes["Outline_Diffuse"].image == None: # fuck you yidhari
                    nodes["Outline_Diffuse"].image = findimg("Tail_Map1_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Tail_Map1_M.png")
                    
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Body Outlines" in mat.name:
                thisisstupid = ["Body_Map1_D.png", "Body_D.png", "Body_1_D.png", "Weapon_Map2_D.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Diffuse"].image = findimg(ugh)
                    if nodes["Outline_Diffuse"].image != None:
                        break
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                
                thisisstupid = ["Body_Map1_M.png", "Body_M.png", "Body_1_M.png", "Weapon_Map2_M.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Lightmap"].image = findimg(ugh)
                    if nodes["Outline_Lightmap"].image != None:
                        break
                    
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Hair Outlines" in mat.name:
                if findimg("Hair_D.png") != None:
                    nodes["Outline_Diffuse"].image = findimg("Hair_D.png")
                    nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'

                    nodes["Outline_Lightmap"].image = findimg("Hair_M.png")
                    nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                    nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Weapon Outlines" in mat.name:
                thisisstupid = ["Weapon_D.png", "Weapon_01_D.png", "Weapon_Map1_D.png", "Weapon_Map2_D.png", "weapon_Map_D.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Diffuse"].image = findimg(ugh)
                    if nodes["Outline_Diffuse"].image != None:
                        break
                if nodes["Outline_Diffuse"].image != None:
                    nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                    
                    thisisstupid = ["Weapon_M.png", "Weapon_01_M.png", "Weapon_Map1_M.png", "Weapon_Map2_M.png", "weapon_Map_M.png"]
                    for ugh in thisisstupid:
                        nodes["Outline_Lightmap"].image = findimg(ugh)
                        print(ugh, findimg(ugh))
                        if nodes["Outline_Lightmap"].image != None:
                            break
                        
                    nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                    nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
            elif "Face Outline" in mat.name:
                nodes["Face_D"].image = bpy.data.materials["ZZZ Shader Face"].node_tree.nodes["Face_D"].image
                
geonode(arm)
outlineshader()


############### ARMATURE RIG SECTION #############
context = bpy.context
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE' and ("avatar" in ob.name.lower() or "npc" in ob.name.lower()):
        obj = ob
if obj.type != 'ARMATURE': # ??? some files just have the rig name as "Armature".
    obj = bpy.data.objects['Armature']
    
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
    
if obj.name[-4:] == ".001":
     obj.name = obj.name[:-4]
print("Rig  Run\n\n")

## Rename all bones in selected armature to ORG
original_name = obj.name
abadidea = {
    'Bip001 Pelvis': 'spine',
    'Bip001 L Thigh': 'thigh.L',
    'Bip001 L Calf': 'shin.L',
    'Bip001 L Foot': 'foot.L',
    'Bip001 L Toe0': 'toe.L',
    'Bip001 R Thigh': 'thigh.R',
    'Bip001 R Calf': 'shin.R',
    'Bip001 R Foot': 'foot.R',
    'Bip001 R Toe0': 'toe.R',
    'Bip001 Spine': 'spine.001',
    'Bip001 Spine1': 'spine.002',
    'Bip001 Spine2': 'spine.003',
    'Bip001 L Clavicle': 'shoulder.L',
    'Bip001 L UpperArm': 'upper_arm.L',
    'Bip001 L Forearm': 'forearm.L',
    'Bip001 L Hand': 'hand.L',
    'Bip001 L Finger0': 'thumb.01.L',
    'DMZ L 01': 'thumb.01.L',  ##WHERE DO THESE SIX COME FROM LMAO
    'DMZ L 02': 'thumb.02.L',
    'DMZ L 03': 'thumb.03.L',
    'DMZ R 01': 'thumb.01.R',
    'DMZ R 02': 'thumb.02.R',
    'DMZ R 03': 'thumb.03.R',    
    'Bip001 L Finger01': 'thumb.02.L',
    'Bip001 L Finger02': 'thumb.03.L',
    'Bip001 L Finger1': 'f_index.01.L',
    'Bip001 L Finger11': 'f_index.02.L',
    'Bip001 L Finger12': 'f_index.03.L',
    'Bip001 L Finger2': 'f_middle.01.L',
    'Bip001 L Finger21': 'f_middle.02.L',
    'Bip001 L Finger22': 'f_middle.03.L',
    'Bip001 L Finger3': 'f_ring.01.L',
    'Bip001 L Finger31': 'f_ring.02.L',
    'Bip001 L Finger32': 'f_ring.03.L',
    'Bip001 L Finger4': 'f_pinky.01.L',
    'Bip001 L Finger41': 'f_pinky.02.L',
    'Bip001 L Finger42': 'f_pinky.03.L',
    'Bip001 Neck': 'spine.004', #YO
    'Bip001 Head': 'spine.006', #RUHROH
    'Bip001 R Clavicle': 'shoulder.R',
    'Bip001 R UpperArm': 'upper_arm.R',
    'Bip001 R Forearm': 'forearm.R',
    'Bip001 R Hand': 'hand.R',
    'Bip001 R Finger0': 'thumb.01.R',
    'Bip001 R Finger01': 'thumb.02.R',
    'Bip001 R Finger02': 'thumb.03.R',
    'Bip001 R Finger1': 'f_index.01.R',
    'Bip001 R Finger11': 'f_index.02.R',
    'Bip001 R Finger12': 'f_index.03.R',
    'Bip001 R Finger2': 'f_middle.01.R',
    'Bip001 R Finger21': 'f_middle.02.R',
    'Bip001 R Finger22': 'f_middle.03.R',
    'Bip001 R Finger3': 'f_ring.01.R',
    'Bip001 R Finger31': 'f_ring.02.R',
    'Bip001 R Finger32': 'f_ring.03.R',
    'Bip001 R Finger4': 'f_pinky.01.R',
    'Bip001 R Finger41': 'f_pinky.02.R',
    'Bip001 R Finger42': 'f_pinky.03.R',
    'EYE_R': 'eye.R',
    'EYE_L': 'eye.L',   
    'Eye_R': 'eye.R',
    'Eye_L': 'eye.L',   
    'Skn_R_Eye': 'eye.R',   
    'Skn_L_Eye': 'eye.L',   
    'Bdy_R_Eye': 'eye.R',
    'Bdy_L_Eye': 'eye.L',   
    'Bdy_R_Eye_Skin': 'eye.R',
    'Bdy_L_Eye_Skin': 'eye.L',   
    'Skn_R_Pupil': 'eye.R',
    'Skn_L_Pupil': 'eye.L',   
    'Skn_Bn_Eye_R': 'eye.R',
    'Skn_Bn_Eye_L': 'eye.L',   
    'Skn_R_Eye_New': 'eye.R',
    'Skn_L_Eye_New': 'eye.L',
    'Bn_Eye_R': 'eye.R',
    'Bn_Eye_L': 'eye.L',
    'PT_L_Eye': 'eye.L',
    'PT_R_Eye': 'eye.R',
    '+Breast L A01': 'breast.L',
    '+Breast R A01': 'breast.R', 
    'Skn_R_Highlights_New': 'Skn_R_Highlights',
    'Skn_L_Highlights_New': 'Skn_L_Highlights',
    }

bpy.ops.object.mode_set(mode='EDIT')
armature = bpy.context.selected_objects[0].data

bpy.ops.armature.select_all(action='DESELECT')
def select_bone(bone):
    bone.select = True
    bone.select_head = True
    bone.select_tail = True
    
select_bone(armature.edit_bones["Bip001 Spine"])
select_bone(armature.edit_bones["Bip001 Spine1"])
select_bone(armature.edit_bones["Bip001 Spine2"])
bpy.ops.armature.parent_clear(type='DISCONNECT')
bpy.ops.armature.select_all(action='DESELECT')

try:
    select_bone(armature.edit_bones["+Breast R A02"])
    select_bone(armature.edit_bones["+Breast L A02"])
    bpy.ops.armature.parent_clear(type='DISCONNECT')
    bpy.ops.armature.select_all(action='DESELECT')
except:
    pass

eb = armature.edit_bones
# fucking knees
eb["Bip001 L Calf"].head[1] -= .005
eb["Bip001 R Calf"].head[1] -= .005

bones_list = obj.pose.bones
for bone in bones_list:
    if bone.name in abadidea:
        bone.name = abadidea[bone.name]


#put hand corection here
import mathutils
bpy.ops.armature.select_all(action='DESELECT')

bpy.context.object.data.use_mirror_x = True
try:
    eb["Skn_R_Mouth"].length = 0.04
    eb["Skn_L_Mouth"].length = 0.04
    eb["Skn_M_Mouth"].length = 0.04
except:
    pass
if eb["hand.L"].tail[0] <= eb["hand.L"].head[0]:
    eb["forearm.L"]
    eb["hand.L"].length = 0.2

    bone_1 = eb["forearm.L"]
    bone_2 = eb["hand.L"]

    direction = (bone_1.tail - bone_1.head).normalized()
    extended_tail_position = bone_1.tail + (direction * 2.0)
    bone_2.tail = extended_tail_position
    bone_2.length = bone_1.length

bpy.context.object.data.use_mirror_x = False

bpy.ops.armature.select_all(action='DESELECT')

        
# Fix finger rolls
how_not = ['f_index.01.L', 'f_index.02.L', 'f_index.03.L']
hahaha = ['f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L']
to_name = ['f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L']
things_efficiently = ['f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L']

for bone in how_not:
    armature.edit_bones[bone].roll -= .1197
    
for bone in hahaha:
    armature.edit_bones[bone].roll -= .04
    
for bone in to_name:
    armature.edit_bones[bone].roll += .1297
    
for bone in things_efficiently:
    armature.edit_bones[bone].roll += .338

if eb["shoulder.L"].roll > -50 and eb["shoulder.L"].roll < 80:
    armature.edit_bones["shoulder.R"].roll = -armature.edit_bones["shoulder.L"].roll 
elif eb["shoulder.R"].roll > -80 and eb["shoulder.R"].roll < 50:
    armature.edit_bones["shoulder.L"].roll = -armature.edit_bones["shoulder.R"].roll 
else:
    eb["shoulder.L"].roll = 0
    eb["shoulder.R"].roll = 0


#Aw shit here we go again.  This second loop is for making it possible to symmetrize pose bones properly.
for bone in bones_list:
    if ".L" in bone.name: 
        whee = bone.name[:-2] + ".R"
        if "f_" in bone.name or "thumb" in bone.name:
            armature.edit_bones[whee].roll = -armature.edit_bones[bone.name].roll
        else:
            lefteye = armature.edit_bones.get("eye.L") # for eyepatched characters
            righteye = armature.edit_bones.get("eye.R")
            if not righteye or not lefteye:
                pass
            else:
                try:
                    armature.edit_bones[bone.name].roll = -armature.edit_bones[whee].roll
                except:
                    pass

# Fixes the thumb scale rotating inward on x instead of z
armature.edit_bones["thumb.01.L"].roll += 3.14 / 4
armature.edit_bones["thumb.02.L"].roll += 3.14 / 4
armature.edit_bones["thumb.03.L"].roll += 3.14 / 4     
armature.edit_bones["thumb.01.R"].roll -= 3.14 / 4
armature.edit_bones["thumb.02.R"].roll -= 3.14 / 4
armature.edit_bones["thumb.03.R"].roll -= 3.14 / 4    

for bone in armature.edit_bones:
    if "thumb" in bone.name or "index" in bone.name or "middle" in bone.name or "ring" in bone.name or "pinky" in bone.name:
        if ".L" in bone.name:
            armature.edit_bones[bone.name].roll -= 1.571 
        else:
            armature.edit_bones[bone.name].roll += 1.571 
    ## Not sure why this bone exist but it's gotta go lmao
    if bone.name == "Bip001": 
        for childbone in bone.children:
            if childbone.name != "spine":
                armature.edit_bones[childbone.name].parent = armature.edit_bones['spine'] 
        armature.edit_bones.remove(bone)
    elif ".L" not in bone.name and ".R" not in bone.name:
        armature.edit_bones[bone.name].roll = 0

        
## Fixes the weirdass pelvis/spine bone.  Sets the spine's head and tail X to 0.  
def realign(bone):
    bone.head.x = 0
    bone.tail.x = 0
realign(armature.edit_bones['spine'])
realign(armature.edit_bones['spine.006'])


## Attaches the feet to the toes and the upperarms to lowerarms
def attachfeets(foot, toe):
    armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x
    armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
    armature.edit_bones[foot].tail.z = armature.edit_bones[toe].head.z

attachfeets('foot.L', 'toe.L')
attachfeets('foot.R', 'toe.R')
attachfeets('upper_arm.L', 'forearm.L')
attachfeets('upper_arm.R', 'forearm.R')
attachfeets('thigh.L', 'shin.L')
attachfeets('thigh.R', 'shin.R') 
attachfeets('forearm.L', 'hand.L')
attachfeets('forearm.R', 'hand.R')
attachfeets('spine', 'spine.001')
attachfeets('spine.001', 'spine.002')
attachfeets('spine.002', 'spine.003')
attachfeets('spine.003', 'spine.004')
attachfeets('spine.004', 'spine.006')

## Points toe bones in correct direction
armature.edit_bones['toe.L'].tail.z = 0
armature.edit_bones['toe.R'].tail.z = 0
armature.edit_bones['toe.L'].tail.y -= 0.05
armature.edit_bones['toe.R'].tail.y -= 0.05
        
bpy.ops.armature.select_all(action='DESELECT')
try:
    select_bone(armature.edit_bones["breast.L"])
    bpy.ops.armature.symmetrize()
    bpy.ops.armature.select_all(action='DESELECT')

except Exception:
    pass

try:
    armature.edit_bones["eye.L"].name = "DEF-eye.L"
    armature.edit_bones["eye.R"].name = "DEF-eye.R"
except:
    pass
bpy.ops.object.mode_set(mode='POSE')

bpy.ops.object.expykit_convert_bone_names(src_preset='Rigify_Metarig.py', trg_preset='Rigify_Deform.py')
bpy.ops.object.expykit_extract_metarig(rig_preset='Rigify_Metarig.py', assign_metarig=True)



## Fixes the tiddy bones.  Expykit, why did you neglect them

metarm = bpy.data.objects["metarig"].data
bpy.ops.object.mode_set(mode='EDIT')
armature = bpy.data.objects[obj.name].data

## Left side first, right side's xyz is same as left, but x is negative
def getboob(bone, tip):
    if tip == "head":
        return armature.edit_bones[bone].head.x, armature.edit_bones[bone].head.y, armature.edit_bones[bone].head.z
    else:
        return armature.edit_bones[bone].tail.x, armature.edit_bones[bone].tail.y, armature.edit_bones[bone].tail.z
        
    
try:
    xh, yh, zh = getboob("breast.L", "head")
    xt, yt, zt = getboob("breast.L", "tail")

    ## Change the meta arm's boob positions

    def fixboob(bone, xh, yh, zh, xt, yt, zt):
        bone.head.x = xh
        bone.head.y = yh
        bone.head.z = zh
        bone.tail.x = xt
        bone.tail.y = yt
        bone.tail.z = zt

    boobL = metarm.edit_bones["breast.L"]
    fixboob(boobL, xh, yh, zh, xt, yt, zt)
    boobR = metarm.edit_bones["breast.R"]
    fixboob(boobR, -xh, yh, zh, -xt, yt, zt)

    boobL.roll = armature.edit_bones["breast.L"].roll
    boobR.roll = -boobL.roll
except Exception:
    # If breast bones dont exist in the orig rig, then delete from the meta rig
    metarm.edit_bones.remove(metarm.edit_bones["breast.L"])
    metarm.edit_bones.remove(metarm.edit_bones["breast.R"])
    
    
    
# Fixes the finger rolls
bpy.ops.object.mode_set(mode='OBJECT')
metapose = bpy.data.objects['metarig'].pose
for bone_name in ['f_index', 'f_middle', 'f_ring', 'f_pinky']:
    metapose.bones[f"{bone_name}.01.L"].rigify_parameters.primary_rotation_axis = 'Z'
    metapose.bones[f"{bone_name}.01.R"].rigify_parameters.primary_rotation_axis = '-Z'
                                                                           
metapose.bones["thumb.01.L"].rigify_parameters.primary_rotation_axis = 'Z'
metapose.bones["thumb.01.R"].rigify_parameters.primary_rotation_axis = '-Z'     

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

armature = obj.data
for o in bpy.data.objects:
    # Check for given object names
    if o.name in ("metarig", armature.name):
        o.select_set(True)

bpy.ops.object.mode_set(mode='EDIT')
for bone in metarm.edit_bones:
    if "f_" in bone.name or "thumb" in bone.name:
        bone.roll =  armature.edit_bones["DEF-"+bone.name].roll


##########  DETACH PHYSICS BONES,  

metanames = ['eye.L', 'eye.R', 'spine', 'thigh.L', 'shin.L', 'foot.L', 'toe.L', 'thigh.R', 'shin.R', 'foot.R', 'toe.R', 'spine.001', 'spine.002', 'spine.003', 'breast.L', 'breast.R', 'shoulder.L', 'upper_arm.L', 'forearm.L', 'hand.L', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'spine.004', 'spine.006', 'shoulder.R', 'upper_arm.R', 'forearm.R', 'hand.R', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R']

pre_res = ["DEF-" + bonename for bonename in metanames]
armature = obj.data ## Original char rig


## Make a dictionary.  Key is a main body bone that exists in the Rigify (arm, leg, spine, etc), and the value is a list of all the children bones that aren't other main body bones (usually hair, clothes, deform, etc.)
savethechildren = {
    
}
bpy.ops.object.mode_set(mode='EDIT')
for bone in armature.edit_bones:
    if bone.name in pre_res:
        childlist = []
        for childbone in armature.edit_bones[bone.name].children:
            if childbone.name not in pre_res: # Adds only non-main body bones, avoids like forearm or knee etc
                childlist.append(childbone.name)
        if childlist: # If list isn't empty, add it to dict
            wtf = bone.name
            savethechildren[wtf] = childlist

    
## Duplicates the physics bones
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_all(action='DESELECT')
bones = armature.edit_bones[:]
for bone in bones:
    if bone.name not in pre_res:
        #this is a physics bone, so duplicate it.
        bone.select = True
        bone.select_tail = True
        bone.select_head = True

bpy.ops.armature.separate()
# Generates rigify rig and renames it to 'rigify'
bpy.ops.pose.rigify_generate()
bpy.data.objects[obj.name].name = "rigify"
bpy.context.view_layer.objects.active = bpy.data.objects[armature.name + ".001"]


for o in bpy.data.objects:
    # Check for given object names
    if o.name in ("rigify", armature.name):
        o.select_set(True)
        
# THEN REATTACH PHYSICS

bpy.ops.object.mode_set(mode='OBJECT')
### BLENDER ARE U GOOD LMAO WTF IS THIS (this joins two objects together)
newrig = armature.name + ".001" ## New temporary armature with the physics bones. Hopefully you didnt touch any names lmao

## Why's the list for selected objects ordered alphabetically instead of by selection order
objList = bpy.context.selected_objects
unselected = [obj for obj in objList if obj != context.active_object]
rigifyr = unselected[0]  ## Rigified Rig

obs = [bpy.data.objects[rigifyr.name], bpy.data.objects[newrig]]
c={}
c["object"] = c["active_object"] = bpy.data.objects[rigifyr.name]
c["selected_objects"] = c["selected_editable_objects"] = obs
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

with bpy.context.temp_override(active_object=bpy.data.objects.get("rigify"), selected_editable_objects=obs):
    bpy.ops.object.join()


bpy.context.view_layer.objects.active = bpy.data.objects["rigify"]
bpy.ops.object.mode_set(mode='EDIT')

## Reattach the physics bones to their parents
#Go back into rigify, find the main body bones, and reattach every bone in the corresponding dict list
for mainbone in savethechildren:    
    for childbone in savethechildren[mainbone]:
        rigifyr.data.edit_bones[childbone].parent = rigifyr.data.edit_bones[mainbone]

print("donelol\n")
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects["rigify"].show_in_front = True

# Symmetrize clothes/hair bones
for bone in rigifyr.data.edit_bones:
    if " L " in bone.name:  # Finds clothes/hair bones with symmetrical bones
        y = bone.name.find(' L ')  # Finds index of "Hair L 1"
        orgname = bone.name
        try:
            oppbone = orgname[:y] + " R " + orgname[y+3:] # oppbone = "Hair R 1"
            bone.name = orgname[:y] + orgname[y+3:] + ".L"  #Rename bones to "Hair 1.L/R" so Blender 
            rigifyr.data.edit_bones[oppbone].name = orgname[:y] + orgname[y+3:] + ".R" # goes ":o symmetry"
        except:
            pass


bpy.ops.object.mode_set(mode='POSE')

rigifyr.pose.bones["upper_arm_parent.L"]["pole_parent"] = 2
rigifyr.pose.bones["upper_arm_parent.R"]["pole_parent"] = 2
rigifyr.pose.bones["thigh_parent.L"]["pole_parent"] = 2
rigifyr.pose.bones["thigh_parent.R"]["pole_parent"] = 2
rigifyr.pose.bones["upper_arm_parent.R"]["pole_vector"] = True
rigifyr.pose.bones["upper_arm_parent.L"]["pole_vector"] = True
rigifyr.pose.bones["thigh_parent.L"]["pole_vector"] = True
rigifyr.pose.bones["thigh_parent.R"]["pole_vector"] = True


bpy.ops.object.mode_set(mode='OBJECT')
#change active object to rigifyr

bpy.context.view_layer.objects.active = bpy.data.objects["rigify"]

bpy.ops.object.mode_set(mode='OBJECT')

# This part puts all the main bones I use into the secoond bone layer
listofbones = ["root", "eye.L", "eye.R", "foot_heel_ik.R", "foot_heel_ik.L", "toe_ik.R", "toe_ik.L", "foot_ik.R", "foot_ik.L", "thigh_ik_target.R", "thigh_ik_target.L", "hips", "torso", "chest", "neck", "head", "shoulder.L", "shoulder.R", "upper_arm_fk.L", "upper_arm_fk.R", "forearm_fk.L", "forearm_fk.R", "hand_fk.L", "hand_fk.R", "upper_arm_ik_target.L", "upper_arm_ik_target.R", "hand_ik.R", "hand_ik.L", "Skn_L_Mouth", "Skn_R_Mouth", "Skn_M_Mouth"]

clothes = ["ribbon", "sleeve", "strap", "skirt", "button", "belt", "cloth", "tail", "bag", "chain", "collar", "cloak", "hat"]
hair = ["hair", "eardrop", "bangs"]
face = ["brow", "mouth", "eye", "ear_"]

eb = obj.pose.bones
bpy.ops.object.mode_set(mode='POSE')
if ver == 3:
    for bone in listofbones:
        bpy.context.active_object.pose.bones[bone].bone.layers[1] = True
        
        # Separates physics-related bones into layers 22 and 23
    for bone in eb:
        for name in clothes:
            if name in bone.name.lower():
                obj.pose.bones[bone.name].bone.layers[22] = True
                obj.pose.bones[bone.name].bone.layers[0] = False
        for name in hair:
            if name in bone.name.lower():
                obj.pose.bones[bone.name].bone.layers[23] = True
                obj.pose.bones[bone.name].bone.layers[0] = False

else:
    bone_collection = rigifyr.data.collections.new(name="Main")
    for bone_name in listofbones:
        bone_collection.assign(rigifyr.pose.bones.get(bone_name))
        
    bpy.ops.pose.select_all(action='DESELECT')
    phys_collection = rigifyr.data.collections.new(name="Clothes")
    hair_collection = rigifyr.data.collections.new(name="Hair")
    misc_collection = rigifyr.data.collections.new(name="Misc")
    for bone in eb:  # search every bone to see if it's a physisc bone by name
        for name in clothes:
            if name in bone.name.lower():
                print(bone.name)
                phys_collection.assign(bone)
        for name in hair:
            if name in bone.name.lower():
                hair_collection.assign(bone)
                
        for name in face:
            if name in bone.name.lower() and "DEF-" not in bone.name and "ORG-" not in bone.name:
                rigifyr.data.collections["Face"].assign(bone)
    
        if not any(bone.name in coll.bones for coll in rigifyr.data.collections):
            misc_collection.assign(bone)
    rigifyr.data.collections.move(26, 0)
    rigifyr.data.collections.move(26, 0)
    rigifyr.data.collections.move(26, 0)
    rigifyr.data.collections.move(26, 0)
    if ver == 4: # version 4.0
        bpy.ops.armature.collection_solo_visibility(name="Main")
    elif ver != 3:
        for c in rigifyr.data.collections:
            c.is_visible = False
        rigifyr.data.collections_all["Main"].is_visible = True
        pass
#    rigifyr.data.collections["Physics"].is_visible = True
#    rigifyr.data.collections["Hair"].is_visible = True

        
bpy.ops.object.mode_set(mode='OBJECT')
x = original_name.split("_")
bpy.data.objects["rigify"].name = x[-1] + "Rig"


bpy.ops.object.mode_set(mode='EDIT')
bones = rigifyr.data.edit_bones[:]

# this bitch empty. YEET
#rigifyr.data.edit_bones.remove(rigifyr.data.edit_bones["palm.L"])
#rigifyr.data.edit_bones.remove(rigifyr.data.edit_bones["palm.R"])

# Change any physics bones attached to shoulder to be attached to spine instead bc it's a pain in the ass
# for bone in bones:
    # if bone.parent:
        # if bone.name not in pre_res and bone.parent.name in ["DEF-shoulder.L", "DEF-shoulder.R"]:
            # print(bone)
            # bone.parent = rigifyr.data.edit_bones["DEF-spine.003"]
        
# makes a root #2 bone
newroot = rigifyr.data.edit_bones.new("root_2")
root = rigifyr.data.edit_bones["root"]
newroot.head = root.head.copy()
newroot.tail = root.tail.copy()
newroot.roll = root.roll
newroot.matrix = root.matrix.copy()
newroot.tail.y += 0.5
root.parent = newroot

bpy.ops.object.mode_set(mode='POSE')   
bpy.ops.pose.select_all(action='DESELECT')
bones_list = obj.pose.bones
bpy.ops.object.mode_set(mode='POSE')
rigifyr.pose.bones["root_2"].custom_shape = bpy.data.objects["WGT-" + original_name + "_root"]

bpy.ops.pose.select_all(action='DESELECT')
bone = rigifyr.pose.bones["root_2"].bone
rigifyr.data.bones.active = bone
if ver == 3:
    bpy.ops.pose.group_assign(type=6)
    for x in range(0, 28):
        bone.layers[x] = False
    bone.layers[1] = True

else:
    rigifyr.data.collections["Main"].assign(rigifyr.pose.bones.get("root_2"))
    rigifyr.data.collections["Root"].assign(rigifyr.pose.bones.get("root_2"))

# Creates selection sets for FK arms + shoulders, hair bones, and clothes bones.  Selection Sets is an addon that comes with Blender.
try:
    bpy.ops.object.mode_set(mode='POSE')

    arms = ['upper_arm_fk', 'forearm_fk', 'hand_fk', 'shoulder']
    bpy.ops.pose.select_all(action='DESELECT')
    for side in ['.L', '.R']:
        for bone in arms:
            bonename = bone + side
            rigifyr.pose.bones[bonename].bone.select= True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')

    ## Hair
    for bone in bones_list:
        if "Hair" in bone.name:
            rigifyr.pose.bones[bone.name].bone.select = True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')

    ## Clothes
    for bone in bones_list:
        if "Amice" in bone.name or ("fk" not in bone.name and "tweak" not in bone.name and "Twist" not in bone.name and "Hair" not in bone.name and (bone.name[-1].isdigit() or bone.name[-3].isdigit())):
            rigifyr.pose.bones[bone.name].bone.select = True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.context.object.selection_sets[0].name = "FK Arms"
    bpy.context.object.selection_sets[1].name = "Hair"
    bpy.context.object.selection_sets[2].name = "Clothes"
except:
    pass

bpy.ops.object.mode_set(mode='OBJECT')
    
rigifyr.pose.bones["upper_arm_parent.L"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["upper_arm_parent.R"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["thigh_parent.L"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["thigh_parent.R"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["torso"]["neck_follow"] = 1.000

rig = rigifyr

for oDrv in rig.animation_data.drivers:
    for variable in oDrv.driver.variables:
        for target in variable.targets:
            if ".03" in oDrv.data_path and target.data_path[-7:] == "scale.y":
                target.data_path = target.data_path[:-1] + "x"


fingerlist = ["thumb.01_master", "f_index.01_master", "f_middle.01_master", "f_ring.01_master", "f_pinky.01_master"]

for side in [".L", ".R"]:
    for bone in fingerlist:
        rig.pose.bones[bone + side].lock_scale[0] = False
        

armature = rig

fucks = ["upper_arm_ik_target.L", "upper_arm_ik_target.R", "VIS_upper_arm_ik_pole.L", "VIS_upper_arm_ik_pole.R", "thigh_ik_target.L", "thigh_ik_target.R", "VIS_thigh_ik_pole.L", "VIS_thigh_ik_pole.R"]
bpy.ops.object.mode_set(mode='POSE')
for fuck in fucks:
    armature.data.bones[fuck].driver_remove("hide")
    
bpy.ops.object.mode_set(mode='EDIT')
for bone in armature.data.edit_bones:
    if "_L_" in bone.name:  # Finds clothes/hair bones with symmetrical bones
        y = bone.name.find('_L_')  # Finds index of "Hair_L_1"
        orgname = bone.name
        try:
            oppbone = orgname[:y] + "_R_" + orgname[y+3:] # oppbone = "Hair_R_1"
            bone.name = orgname[:y] + orgname[y+3:] + ".L"  #Rename bones to "Hair 1.L/R" so Blender 
            armature.data.edit_bones[oppbone].name = orgname[:y] + orgname[y+3:] + ".R" # goes ":o symmetry"
#            print(orgname, oppbone)
        except:
            pass

bpy.ops.object.mode_set(mode='OBJECT')

bpy.data.objects["Head Up"].hide_viewport = True
bpy.data.objects["Head Forward"].hide_viewport = True

bpy.context.object.name = charname + "Rig"



bpy.data.objects["Head Direction"].constraints["Child Of"].target = rigifyr
bpy.data.objects["Head Direction"].constraints["Child Of"].subtarget = "DEF-spine.006"

    
for obj in ["Lighting Panel", "Head Direction", "Light Direction", "Head Up", "Head Forward"]:
    bpy.data.objects[obj].name = charname + obj
    
rig.users_collection[0].name = charname[:-1]

# Join the light rig to the character rig
active_rig = bpy.context.object
lighting_panel_rig = bpy.data.objects.get(charname + "Lighting Panel")
bpy.ops.object.select_all(action='DESELECT')
lighting_panel_rig.select_set(True)
active_rig.select_set(True)
bpy.context.view_layer.objects.active = active_rig
bpy.ops.object.join()


for obj in [obj for obj in bpy.data.objects if "ColorWheel-" in obj.name]:
    drv = obj.animation_data.drivers[0]
    drv.driver.variables[0].targets[0].id = bpy.context.object.data
    if ver == 3:
        obj.animation_data.drivers.find("hide_viewport").driver.variables[0].targets[0].data_path = 'layers[0]'
    else:
        obj.animation_data.drivers.find("hide_viewport").driver.variables[0].targets[0].data_path = 'collections["Light Panel"].is_visible'  
    

if ver != 3:
    rigifyr.data.collections.move(27, 0)
    rigifyr.data.collections["Light Panel"].is_visible = True
    rigifyr.data.collections["Light Panel Extras"].is_visible = False


## FACERIG STUFF
import bpy
import mathutils
print("RAAAAGH\n\n")


#for obj in bpy.data.objects:
#    if "_face" in obj.name and obj.type == 'MESH' and obj.parent.type == 'ARMATURE':
#        faceobj = obj

def shapekeyrename(keyblock):
    # rename inconsistent shapekeys, especially in older characters
    for sk in keyblock:
        if sk.name.endswith("_Unagi") or sk.name.endswith("_Anton") or sk.name.endswith("_Corin"): # miyabi, what the actual fuck
            sk.name = sk.name[:-6]
        if sk.name.endswith("_NuoCha"): # nicole, what the actual fuck
            sk.name = sk.name[:-7]
    dick = {
        "Mouth_↖_Ben" : "Fac_Mth_R_Up",
        "Mouth_↗_Ben" : "Fac_Mth_L_Up",
        "Mouth_↙_Ben": "Fac_Mth_R_Down", 
        "Mouth_↘_Ben": "Fac_Mth_L_Down", 
        "Mouth_上颌↑_Ben" : "Fac_Mth_Up", 
        "Mouth_下颌↓_Ben" : "Fac_Mth_Down", 
        "Mouth_呲_L_Ben" : "Fac_Mth_L_In", 
        "Mouth_呲_R_Ben" : "Fac_Mth_R_In", 
        "Eye_Open_↑_Ben": "Fac_Eye_R_Open",
        "Mouth_Oo_Ben": "Fac_Mth_UuOo",
        "Eye_Close2_Ben": "Fac_Eye_Sad",
        "Eye_Ball_↑_Ben": "Eye_Up",
        "Eye_Ball_↓_Ben": "Eye_Down",
        "Eye_Ball_→_Ben": "Eye_Left",
        "Eye_Ball_←_Ben": "Eye_Right",
        "Eye_Ball_No_Ben": "O_O",
        "Mouth_啧_R_Ben": "Fac_Mth_R_Out",
        "Mouth_啧_L_Ben": "Fac_Mth_L_Out" ,
        "Mouth_Ii1": "Fac_Mth_Ii",
        
        "Fac_Mth_Aa" : "Fac_Mth_Aa1", 
        "Fac_Mth_ooR" : "Fac_Mth_R_Out", 
        "Fac_Mth_Roo" : "Fac_Mth_R_In", 
        "Fac_Mth_Loo" : "Fac_Mth_L_Out", 
        "Fac_Mth_ooL" : "Fac_Mth_L_In", 
        "Fac_Mth_oo_RDown": "Fac_Mth_R_Down", 
        "Fac_Mth_LDown_oo": "Fac_Mth_L_Down", 
        "Fac_Mth_LUp_oo" : "Fac_Mth_L_Up",
        "Fac_Eye_Open_L" : "Fac_Eye_L_Open",
        "Fac_Eye_LowEyeUP" : "Fac_Eye_LowlidUp",
        "Fac_Eye_LowEyeUP" : "Fac_Eye_LowlidUp",
        "Fac_Mth_Laugh1" : "Fac_Mth_Laugh",
        
        ## NICOLE MIYABI WTF
        "EB_↑" : "Fac_Ebr_Up",
        "EB_↓" : "Fac_Ebr_Down", 
        "EB_Angry" : "Fac_Ebr_Angry", 
        "EB_Relax" : "Fac_Ebr_Relax", 
        "EB_困扰" : "Fac_Ebr_Sad", 
        "Eye_↙↘" : "Fac_Eye_BLBR",
        "Eye_Angry" : "Fac_Eye_Angry", 
        "Eye_Close" : "Fac_Eye_Close", 
        "Eye_Open_L" : "Fac_Eye_L_Open", 
        "Eye_Open_R" : "Fac_Eye_R_Open", 
        "Eye_Wink_L" : "Fac_Eye_L_Wink", 
        "Eye_Wink_R" : "Fac_Eye_R_Wink", 
        "EYE_Wink_L" : "Fac_Eye_L_Wink", 
        "EYE_Wink_R" : "Fac_Eye_R_Wink", 
        "Eye_半闭" : "Fac_Eye_HalfClose", 
        "Eye_困扰" : "Fac_Eye_Sad",
        "Eye_认真" : "Fac_Eye_MidDown",
        "Eye_下眼睑↑" : "Fac_Eye_LowlidUp", 
        "Mouth_△" : "Fac_Mth_Triangle", 
        "Mouth_↑" : "Fac_Mth_Up", 
        "Mouth_→" : "Fac_Mth_Left", 
        "Mouth_↓" : "Fac_Mth_Down", 
        "Mouth_←" : "Fac_Mth_Right", 
        "Mouth_Aa1" : "Fac_Mth_Aa1",
        "Mouth_Aa2" : "Fac_Mth_Aa2",
        "Mouth_Aa3Shout" : "Fac_Mth_Aa3Shout",
        "Mouth_AaTalk" : "Fac_Mth_AaTalk",
        "Mouth_Ee" : "Fac_Mth_Ee",
        "Mouth_Ii" : "Fac_Mth_Ii",
        "Mouth_Uu_Ben" : "Fac_Mth_Uu",
        "Mouth_Laugh" : "Fac_Mth_Laugh",
        "Mouth_Laugh2" : "Fac_Mth_Laugh2",
        "Mouth_oo←" : "Fac_Mth_L_In",
        "Mouth_↖oo" : "Fac_Mth_L_Up",
        "Mouth_←oo" : "Fac_Mth_R_Out",
        "Mouth_↙oo" : "Fac_Mth_R_Down",
        "Mouth_→oo" : "Fac_Mth_R_In",
        "Mouth_oo↗" : "Fac_Mth_R_Up",
        "Mouth_oo→" : "Fac_Mth_L_Out",
        "Mouth_oo↘" : "Fac_Mth_L_Down",
        "Mouth_Oo" : "Fac_Mth_Oo",
        "Mouth_Uu" : "Fac_Mth_Uu",
        "Mouth_UuOo" : "Fac_Mth_UuOo",
        
    }
    
    for key in dick.keys():
        try:
            keyblock[key].name = dick[key]  # change keyname to valuename
        except:
            for sk in keyblock:
                if key in sk.name:
                    sk.name = dick[key]
            pass

    for sk in keyblock:
        if sk.name.endswith("_Ben"): # put ben here bc this makes things easier.
            sk.name = sk.name[:-4]
            
def create_facerig_with_lim_bones(keyblock):
    shapekeys = [sk.name[4:] for sk in keyblock if "Fac_" in sk.name] # List of shapekey names without 'Fac_'
    for sk in keyblock:
        if "Fac_" not in sk.name and sk.name != "Basis":
            shapekeys.append(sk.name)
            sk.name = "Fac_" + sk.name  # starting to regret not just removing 'fac' from the shapekey names lol
        
    bpy.ops.object.armature_add()  # Create a new armature
    armature = bpy.context.object
    armature.name = "FaceRig"
    armature.data.name = "FaceRig"
    armature.parent = bpy.data.objects["Facerig Border"]    
    armature.matrix_parent_inverse = bpy.data.objects["Facerig Border"]   .matrix_world.inverted()
    
    
    bpy.ops.object.mode_set(mode='EDIT')  # Switch to edit mode
    armature.data.edit_bones.remove(armature.data.edit_bones["Bone"])
    faceroot = armature.data.edit_bones.new("Facerig Root")
    faceroot.head = (2, 0, 1.18)
    faceroot.tail = (2, 0, 1.48)
    
    for obj in bpy.data.objects:
        # Deal with extra shapekeys not in the base facerig
        if obj.name in shapekeys:
            shapekeys.remove(obj.name)
    print(shapekeys)

    for i in range(1, len(shapekeys)+1):
        text = bpy.data.objects["Extra " + str(i)]
        text.name = shapekeys[i-1]
        text.data.name = shapekeys[i-1]
        text.data.body = shapekeys[i-1]
        
        textlim = bpy.data.objects["Extra " + str(i) + " lim"]
        textlim.name = shapekeys[i-1] + " lim"
        textlim.data.name = shapekeys[i-1] + " lim"
        
    for obj in bpy.data.objects:
        if 'lim' in obj.name and ("Fac_" + obj.name[:-4]) in keyblock or (obj.name == "Mth lim"):  #  Makes a new bone if there's actually a shapekey for it
            bone = armature.data.edit_bones.new(obj.name[:-4] + " Bone")
            bone.head = obj.location  # Set bone head position
            bone.tail = obj.location + mathutils.Vector((0, 0, 0.1))  # Set bone tail position slightly above head
            bone.parent = armature.data.edit_bones["Facerig Root"]
        
    armature = bpy.data.objects["FaceRig"]
    
    bpy.ops.object.mode_set(mode='POSE')  
    
    for bone in armature.pose.bones:
        if ver != 3:
            armature.data.collections[0].assign(bone)
        if bone.name == "Facerig Root":
            continue
        bone.custom_shape = bpy.data.objects["Mth lim"]
        bone.custom_shape_scale_xyz[1] = 0.2
        bone.custom_shape_scale_xyz[2] = 0.2
        bone.custom_shape_scale_xyz[0] = 0.2
        
        # Lock transformations, rotation, and scale except X-axis
        if bone.name != "Mth Bone":
            bone.lock_location[1] = True
        bone.lock_location[2] = True
        bone.lock_rotation[0] = True
        bone.lock_rotation[1] = True
        bone.lock_rotation[2] = True
        bone.lock_scale[0] = True
        bone.lock_scale[1] = True
        bone.lock_scale[2] = True
        
        # Add limit location constraint
        if bone.name != "Mth Bone":
            constraint = bone.constraints.new(type='LIMIT_LOCATION')
            constraint.use_min_x = True
            constraint.use_max_x = True
            constraint.min_x = -0.1
            constraint.max_x = 0.1
            constraint.use_transform_limit = True
            constraint.owner_space = 'LOCAL'
        else:    
            constraint = bone.constraints.new(type='LIMIT_DISTANCE')
            constraint.distance = 0.1
            constraint.target = bpy.data.objects["Mth lim"]
    
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode

def facestuff(mesh_obj):
    for shapekey in mesh_obj.data.shape_keys.key_blocks:
        if shapekey.name == "Basis":
            continue
        
        bone_name = shapekey.name
        shapekey.slider_min = -1.0
        
        if "Fac_" in bone_name:
            bone_name = bone_name[4:]
        if (bone_name + " Bone") in bpy.data.objects["FaceRig"].data.bones:

            driver = shapekey.driver_add("value").driver
            driver.type = 'SCRIPTED'
            var = driver.variables.new()
            var.name = "var"
            var.type = 'TRANSFORMS'
            target = var.targets[0]
            target.id = bpy.data.objects["FaceRig"]
            target.bone_target = bone_name + " Bone"
            target.transform_type = 'LOC_X' 
            target.transform_space = 'LOCAL_SPACE'
            
            driver.expression = "var / 0.1"

def mouthbone(keyblock):
    bone = bpy.data.objects["FaceRig"].data.bones["Mth Bone"]    

    sklist = ["Fac_Mth_Up","Fac_Mth_Left","Fac_Mth_Right","Fac_Mth_Down"]
    
    for shapekey in sklist: 
        if shapekey not in keyblock:
            continue
        keyblock[shapekey].slider_min = 0.0
        
        driver = keyblock[shapekey].driver_add("value").driver
        driver.type = 'SCRIPTED'
        var = driver.variables.new()
        var.name = "var"
        var.type = 'TRANSFORMS'
        target = var.targets[0]
        target.id = bpy.data.objects["FaceRig"]
        target.bone_target = bone.name
        target.transform_space = 'LOCAL_SPACE'
        if "_L" in shapekey or "_R" in shapekey:
            target.transform_type = 'LOC_X' 
        else:
            target.transform_type = 'LOC_Y' 
        if "_L" in shapekey or "_Up" in shapekey:
            driver.expression = "var / 0.1"
        else:
            driver.expression = "-var / 0.1"

keyblock = faceobj.data.shape_keys.key_blocks
            
shapekeyrename(keyblock)            
create_facerig_with_lim_bones(keyblock)
facestuff(faceobj)
mouthbone(keyblock)


def gdilycaon(): # Lycaon's mask has shapekeys. need to copy drivers.
    for shapekey in bpy.data.objects["Lycaon_Body_3"].data.shape_keys.key_blocks:
        if "_Body" in shapekey.name:
            shapekey.name = shapekey.name[:-5]
    facestuff(bpy.data.objects["Lycaon_Body_3"])    
    
try:
    gdilycaon()
except:
    pass                        

# Join the facerig to the main rig

if ver != 3:
    bpy.data.objects["FaceRig"].data.collections["Bones"].name = "Facerig"
active_rig = rigifyr
lighting_panel_rig = bpy.data.objects.get("FaceRig")
bpy.ops.object.select_all(action='DESELECT')
lighting_panel_rig.select_set(True)
active_rig.select_set(True)
bpy.context.view_layer.objects.active = active_rig
bpy.ops.object.join()

if ver != 3:
    rigifyr.data.collections.move(29, 0)

border = bpy.data.objects["Facerig Border"]
border.constraints["Child Of"].target = rigifyr
border.constraints["Child Of"].subtarget = "Facerig Root"

bpy.context.view_layer.objects.active = border
bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT')


bpy.context.view_layer.objects.active = rigifyr
bpy.ops.object.mode_set(mode='POSE')  

con = rigifyr.pose.bones["Facerig Root"].constraints.new(type='CHILD_OF')
con.target = rigifyr
con.subtarget = "DEF-spine.006"

con = rigifyr.pose.bones["Lighting Panel"].constraints.new(type='CHILD_OF')
con.target = rigifyr
con.subtarget = "DEF-spine.006"

from mathutils import Vector
obj = bpy.context.object

if obj and obj.type == 'ARMATURE': #to relocate and scale the facerig root position
    pbone = obj.pose.bones.get("Facerig Root")
    if pbone:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='POSE')
        pbone.location.x -= 0.9
        pbone.location.y += 0.3
        pbone.scale = Vector((0.5, 0.5, 0.5))

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = rigifyr.data.edit_bones


### EYE RIG PART
eyes = True
if "eye.R" not in rigifyr.pose.bones and "eye.L" not in rigifyr.pose.bones:
    eyes = False

if eyes:
    if "eye.L" in rigifyr.pose.bones:
        original_bone = edit_bones["eye.L"]
        new_bone = edit_bones.new("Eye Control")
        
    elif "eye.R" in rigifyr.pose.bones:
        original_bone = edit_bones["eye.R"]
        new_bone = edit_bones.new("Eye Control")
        
    new_bone.use_inherit_rotation = False
    new_bone.parent = edit_bones["DEF-spine.006"]
    new_bone.name = "Eye Control"
    new_bone.head = original_bone.head
    new_bone.tail = original_bone.tail
    new_bone.head.x = 0
    new_bone.tail.x = 0
    new_bone.head.z = new_bone.tail.z
    new_bone.head.y -= 0.1
    new_bone.tail.y -= 0.15
    new_bone.head[2] = original_bone.head[2]
    new_bone.tail[2] = original_bone.head[2]
    new_bone.length = .07

# Switch to pose mode to set custom shape
bpy.ops.object.mode_set(mode='POSE')
if eyes:
    if ver != 3:
        rigifyr.data.collections["Main"].assign(rigifyr.pose.bones.get("Eye Control"))
        rigifyr.data.collections["Face"].assign(rigifyr.pose.bones.get("Eye Control"))
    pose_bone = rigifyr.pose.bones["Eye Control"]
    pose_bone.custom_shape = rigifyr.pose.bones["thigh_ik_target.L"].custom_shape
    eye_bones = ["eye.L", "eye.R"]
    for bone_name in eye_bones:
        try:
            pose_bone = rigifyr.pose.bones[bone_name]
            constraint = pose_bone.constraints.new(type='CHILD_OF')
            constraint.target = rigifyr
            constraint.subtarget = "Eye Control"
            constraint.use_location_x = False
            constraint.use_location_y = False
            constraint.use_location_z = False
            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False
        except:
            pass
    pose_bone = rigifyr.pose.bones["Eye Control"] ### For eye shrink shapekeys later
    constraint = pose_bone.constraints.new(type='LIMIT_SCALE')
    constraint.use_min_x = True
    constraint.use_min_y = True
    constraint.use_min_z = True
    constraint.min_x = 0.100
    constraint.min_y = 0.100
    constraint.min_z = 0.100

if ver != 3:
    rigifyr.data.collections.remove(rigifyr.data.collections["Face (Primary)"])
    rigifyr.data.collections.remove(rigifyr.data.collections["Face (Secondary)"])

    for c in rigifyr.data.collections:
        if c.rigify_ui_row:
           c.rigify_ui_row -= 3

    rigifyr.data.collections["Main"].rigify_ui_row = 1
    rigifyr.data.collections["Light Panel"].rigify_ui_row = 1
    rigifyr.data.collections["Face"].rigify_ui_row = 2
    rigifyr.data.collections["Facerig"].rigify_ui_row = 2

    rigifyr.data.collections["Torso"].rigify_ui_row = 4
    rigifyr.data.collections["Torso (Tweak)"].rigify_ui_row = 4
    rigifyr.data.collections["Torso (Tweak)"].rigify_ui_title = "Torso (Tweak)"

    rigifyr.data.collections["Fingers"].rigify_ui_row = 5
    rigifyr.data.collections["Fingers (Detail)"].rigify_ui_row = 5
    rigifyr.data.collections["Fingers (Detail)"].rigify_ui_title = "Fing (Detail)"

    rigifyr.data.collections["Root"].rigify_ui_row = 15
    rigifyr.data.collections["Clothes"].rigify_ui_row = 16
    rigifyr.data.collections["Hair"].rigify_ui_row = 16
    rigifyr.data.collections["Misc"].rigify_ui_row = 17


bpy.context.view_layer.objects.active = bpy.data.objects[charname + "Head Direction"]
bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT')

bpy.ops.object.mode_set(mode='OBJECT')  


# Hide facerig objects depending on bone layer visibility
armature = rigifyr
for obj in bpy.data.collections["Facerig"].objects:
    fcurve = obj.driver_add("hide_viewport")
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    driver.expression = "not vis"

    var = driver.variables.new()
    var.name = "vis"
    var.type = 'SINGLE_PROP'
    target = var.targets[0]
    target.id_type = 'ARMATURE'
    target.id = armature.data
    if ver == 3:
        target.data_path = f'layers[0]'
    else:
        target.data_path = f'collections["Facerig"].is_visible'


## This next part adds the eye shrink stuff
if eyes:
    bpy.context.view_layer.objects.active = faceobj
    faceobj.shape_key_add(name="ShrinkEye.R")
    faceobj.shape_key_add(name="ShrinkEye.L")

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

    for side in ['R', 'L']:   # Shrink the eye vertices to make the shrink shapekeys
        notthisshitagain = ["DEF-eye." + side, "eye." + side + ".002", "eye." + side, "eye." + side + ".001", "SknHighlights." + side, "SknHighlights_New." + side]
        bpy.ops.mesh.select_all(action='DESELECT')
        for vg in notthisshitagain:
            if vg in faceobj.vertex_groups:
                if side == 'R':
                    faceobj.active_shape_key_index = len(faceobj.data.shape_keys.key_blocks)-2
                else:
                    faceobj.active_shape_key_index = len(faceobj.data.shape_keys.key_blocks)-1            
                group_index = faceobj.vertex_groups[vg].index
                bpy.ops.object.vertex_group_set_active(group=vg)
                bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(0.2, 0.2, 0.2))
            
    faceobj.active_shape_key_index = 0
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')
    bone_name = "Eye Control"
    shape_keys = faceobj.data.shape_keys.key_blocks

    for shapekey in ["ShrinkEye.L", "ShrinkEye.R"]:
        sk = shape_keys[shapekey]
        
        driver = sk.driver_add("value").driver
        var = driver.variables.new()
        var.name = 'var'
        var.type = 'TRANSFORMS'
        var.targets[0].id = armature  # The object the bone belongs to
        var.targets[0].bone_target = bone_name
        var.targets[0].transform_type = 'SCALE_X'
        var.targets[0].transform_space = 'LOCAL_SPACE'
        driver.expression = '(-10*var)/9 + 10/9'
    
    
    
### THIS PART CONNECTS THE FACESHADOW STUFF TO A NEW BONE
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

# Create new bone
new_bone = rig.data.edit_bones.new("FaceShadow X-Y")

# Set bone head and tail positions
new_bone.head = (0.0, 0.0, 1.73)
new_bone.tail = (0.0, 0.0, 1.89)

bpy.ops.object.mode_set(mode='POSE')
rigifyr.pose.bones["FaceShadow X-Y"].location[0] = -0.002759
rigifyr.pose.bones["FaceShadow X-Y"].location[1] = -0.003272
rigifyr.pose.bones["FaceShadow X-Y"].lock_location[2] = True

if ver != 3:
    rigifyr.data.collections["Facerig"].assign(rigifyr.pose.bones.get("FaceShadow X-Y"))
else:
    for x in range(0, 28):
        rigifyr.pose.bones["FaceShadow X-Y"].bone.layers[x] = False
    rigifyr.pose.bones["FaceShadow X-Y"].bone.layers[0] = True

con = rigifyr.pose.bones["FaceShadow X-Y"].constraints.new(type='CHILD_OF')
con.target = rigifyr
con.subtarget = "DEF-spine.006"

targets = [
    ("Math.004", 0, "location[0]"),  # X location
    ("Math.008", 0, "location[1]"),  # Y location
]
ng=bpy.data.node_groups.get("Face Shader")
for node_name, input_index, bone_axis in targets: # Driver to connect the bone to the faceshadow position
    node = ng.nodes.get(node_name)
    fcurve_path = f'nodes["{node_name}"].inputs[{input_index}].default_value'
    driver = ng.driver_add(fcurve_path).driver
    driver.type = 'SCRIPTED'
    driver.expression = "-var / 5"
    var = driver.variables.new()
    var.name = "var"
    target = var.targets[0]
    target.id = rigifyr
    target.data_path = f'pose.bones["FaceShadow X-Y"].{bone_axis}'
    target.bone_target = "FaceShadow X-Y"
    target.transform_type = 'LOC_X' if bone_axis == "location[0]" else 'LOC_Y'
    target.transform_space = 'LOCAL_SPACE'
bpy.data.materials["ZZZ Shader Face"].blend_method = 'CLIP'

faceobj.modifiers[2].name = """Extra FX (ALL EXCEPT LAST 2 IS FACE ONLY"""
faceobj.modifiers[2].show_in_editmode = False

def eyehighlight():
    bpy.ops.object.mode_set(mode='OBJECT')
    faceobj.active_material_index = len(faceobj.data.materials)-1
    bpy.context.view_layer.objects.active = faceobj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    vertex_groups = ['SknHighlights.R', 'SknHighlights.L']
    for group_name in vertex_groups:
        bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_select()
    for x in range(5):
        bpy.ops.mesh.select_more() # fucking Yidhari has only part of her highlight assigned correctly so i have to do this shit.
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.materials["ZZZ Shader EyeHighlights"].node_tree.nodes["Face_D"].image = bpy.data.materials["ZZZ Shader Face"].node_tree.nodes["Face_D"].image


eyebrowobj = None
for obj in armature.children:
    if obj.name.lower().endswith("_eyebrow"):
        eyebrowobj = obj
        
if eyebrowobj is not None:
    bpy.context.view_layer.objects.active = faceobj
    eyebrowobj.select_set(True)
    faceobj.select_set(True)
    bpy.ops.object.join()

if "SknHighlights.R" in faceobj.vertex_groups: # check if eyehighlights (new chars) are in model
    faceobj.data.materials.append(bpy.data.materials['ZZZ Shader EyeHighlights'])
    eyehighlight()
    
if ver == 3:
    bpy.ops.armature.armature_layers(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

bpy.ops.object.mode_set(mode='OBJECT')
for a in bpy.data.objects:
    if a.type == 'MESH' and a.name.lower().endswith('_face') and "weapon_" not in a.name.lower() and "gun_" not in a.name.lower(): # gdi orphie:
        obj = a 

obj.vertex_groups.new(name="No OL")

mod = obj.modifiers.new("Outlines", "SOLIDIFY")
mod.offset = 1
mod.thickness = 0.001
mod.use_flip_normals = True
mod.material_offset = 1
mod.vertex_group = "No OL"
mod.invert_vertex_group = True
mod.use_rim = False

bod = None
for x in rigifyr.children: # This is for finding the main body object to connect outline viewport drivers
    if "body_1" in x.name.lower() or obj.name[-5:].lower() == "_body" or obj.name.endswith("Body1"):  
        bod = x

for x in rigifyr.children:
    if x == bod:
        continue
    try:
        if x.modifiers[2].name == "Outlines":
            add_driver(x, bod, 'modifiers["Outlines"].show_viewport', 'modifiers["Outlines"].show_viewport')
        elif x.modifiers[3].name == "Outlines": # The face
            add_driver(x, bod, 'modifiers["Outlines"].show_viewport', 'modifiers["Outlines"].show_viewport')
    except:
        pass

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj  # Set as active object

mats = obj.data.materials
origlen = len(mats)
# Traverse each mat, decide what type of outline to use.

for i in range(origlen): # 5 times
    bpy.ops.object.material_slot_add()

for i in range(origlen*2-2, 0, -2): # 8, 6, 4, 2
    for b in range(0, i):
        bpy.ops.object.material_slot_move(direction='UP')
    obj.active_material_index = len(obj.data.materials)-1

for i in range(0, len(obj.data.materials)-1, 2):
    mat = obj.data.materials[i]
    hohoho = None
    if mat.name == "ZZZ Shader Face":
        hohoho = bpy.data.materials["ZZZ Face Outlines"]
    elif mat.name == "ZZZ Shader EyeHighlights" or mat.name == "Eye Transparent":
        hohoho = bpy.data.materials["Transp OL"]
    obj.data.materials[i+1] = hohoho
    
for obj in bpy.data.objects:
    if "metarig" in obj.name:
        obj.hide_viewport = True
        obj.hide_render = True
        
bpy.ops.object.select_all(action='DESELECT') #cleanup
obj = bpy.data.objects.get("Shader Materials (delete later)")
if obj:
    obj.select_set(True)
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)