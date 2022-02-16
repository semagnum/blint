SEVERITY_ERROR = 'ERROR'
SEVERITY_INFO = 'INFO'

lint_rules = [
    {
        'description': 'Default cube exists',
        'severity_icon': SEVERITY_INFO,
        'category_icon': 'MESH_CUBE',
        'issue_expr': '"Cube" in bpy.context.scene.objects',
        'fix_expr': 'bpy.ops.object.select_all(action="DESELECT"); bpy.context.scene.objects["Cube"].select_set('
                    'True); context.view_layer.objects.active = bpy.context.scene.objects["Cube"]; '
                    'bpy.ops.object.delete()',
        'prop_label_expr': ''
    },
    {
        'description': 'extra numerics in name (usually from duplication)',
        'severity_icon': SEVERITY_INFO,
        'category_icon': 'OBJECT_DATA',
        'issue_expr': 'o.name.split(".")[-1].isnumeric()',
        'fix_expr': '',
        'prop_label_expr': 'name',
        'iterable_expr': 'bpy.context.scene.objects',
        'iterable_var': 'o'
    },
    {
        'description': 'Animated seed is disabled',
        'severity_icon': SEVERITY_INFO,
        'category_icon': 'TIME',
        'prop_label_expr': '',
        'issue_expr': 'bpy.context.scene.render.engine == "CYCLES" and not bpy.context.scene.cycles.use_animated_seed',
        'fix_expr': 'bpy.context.scene.cycles.use_animated_seed = True'
    }
]