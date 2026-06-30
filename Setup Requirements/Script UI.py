import bpy

SCRIPT_1_TEXT_NAME = #1 Setup shader, rig, and outline
SCRIPT_2_TEXT_NAME = Jideeh's Setup

BETTER_FBX_OPERATOR_IDS = [
    better_import.fbx,
    better_fbx.import_fbx,
    import_scene.better_fbx,
    import_scene.betterfbx,
    betterfbx.import_scene,
    betterfbx.import_fbx,
]

def disable_auto_keying()
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = False

def run_text_block(text_name)
    text_block = bpy.data.texts.get(text_name)

    if text_block is None
        available_texts = [text.name for text in bpy.data.texts]
        raise RuntimeError(f'Could not find a text block named {text_name}. Available text blocks {available_texts}')

    namespace = {
        __name__ __main__,
        __file__ text_name,
        bpy bpy,
    }

    exec(text_block.as_string(), namespace)

def operator_exists(operator_id)
    parts = operator_id.split(.)

    if len(parts) != 2
        return False

    category_name, operator_name = parts
    category = getattr(bpy.ops, category_name, None)

    if category is None
        return False

    operator = getattr(category, operator_name, None)

    return operator is not None

def call_operator(operator_id)
    category_name, operator_name = operator_id.split(.)
    category = getattr(bpy.ops, category_name)
    operator = getattr(category, operator_name)
    return operator(INVOKE_DEFAULT)

def run_better_fbx_importer()
    for operator_id in BETTER_FBX_OPERATOR_IDS
        if operator_exists(operator_id)
            return call_operator(operator_id)

    raise RuntimeError(
        Could not find the Better FBX Importer operator. 
        Open Blender's Python console, run the Better FBX importer once, 
        then check the operator name in the Info log and add it to BETTER_FBX_OPERATOR_IDS.
    )

class JIDEEH_OT_run_better_fbx_importer(bpy.types.Operator)
    bl_idname = jideeh.run_better_fbx_importer
    bl_label = Better FBX Importer
    bl_options = {REGISTER, UNDO}

    def execute(self, context)
        try
            disable_auto_keying()
            result = run_better_fbx_importer()
            self.report({INFO}, Better FBX Importer opened.)
            return result
        except Exception as error
            self.report({ERROR}, str(error))
            raise

class JIDEEH_OT_run_setup_shader_rig_outline(bpy.types.Operator)
    bl_idname = jideeh.run_setup_shader_rig_outline
    bl_label = Rig, Outline, Shaders
    bl_options = {REGISTER, UNDO}

    def execute(self, context)
        try
            disable_auto_keying()
            run_text_block(SCRIPT_1_TEXT_NAME)
            disable_auto_keying()
            self.report({INFO}, f'Ran {SCRIPT_1_TEXT_NAME}.')
            return {FINISHED}
        except Exception as error
            self.report({ERROR}, str(error))
            raise

class JIDEEH_OT_run_jideeh_setup(bpy.types.Operator)
    bl_idname = jideeh.run_jideeh_setup
    bl_label = Jideeh's Setup
    bl_options = {REGISTER, UNDO}

    def execute(self, context)
        try
            disable_auto_keying()
            run_text_block(SCRIPT_2_TEXT_NAME)
            disable_auto_keying()
            self.report({INFO}, f'Ran {SCRIPT_2_TEXT_NAME}.')
            return {FINISHED}
        except Exception as error
            self.report({ERROR}, str(error))
            raise

class JIDEEH_PT_script_runner_panel(bpy.types.Panel)
    bl_label = Jideeh Script Runner
    bl_idname = JIDEEH_PT_script_runner_panel
    bl_space_type = VIEW_3D
    bl_region_type = UI
    bl_category = Item

    def draw(self, context)
        layout = self.layout
        layout.operator(jideeh.run_better_fbx_importer, text=Better FBX Importer)
        layout.separator()
        layout.operator(jideeh.run_setup_shader_rig_outline, text=Rig, Outline, Shaders)
        layout.operator(jideeh.run_jideeh_setup, text=Jideeh's Setup)

classes = (
    JIDEEH_OT_run_better_fbx_importer,
    JIDEEH_OT_run_setup_shader_rig_outline,
    JIDEEH_OT_run_jideeh_setup,
    JIDEEH_PT_script_runner_panel,
)

def enable_register_on_this_text()
    markers = [
        JIDEEH_PT_script_runner_panel,
        jideeh.run_setup_shader_rig_outline,
        jideeh.run_jideeh_setup,
        jideeh.run_better_fbx_importer,
    ]

    for text in bpy.data.texts
        body = text.as_string()

        if all(marker in body for marker in markers)
            text.use_module = True
            return text.name

    return None

def register()
    disable_auto_keying()

    for cls in classes
        try
            bpy.utils.unregister_class(cls)
        except Exception
            pass

    for cls in classes
        bpy.utils.register_class(cls)

    enabled_text_name = enable_register_on_this_text()

    if enabled_text_name
        print(f'Auto-register enabled for text block {enabled_text_name}')
    else
        print(Could not automatically find this text block to enable Register.)

    print(Auto-keying disabled.)

def unregister()
    for cls in reversed(classes)
        try
            bpy.utils.unregister_class(cls)
        except Exception
            pass

if __name__ == __main__
    register()