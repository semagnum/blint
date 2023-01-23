import bpy

from ..model.icon_gen import get_icons, format_icon_name


class BT_OT_SelectIcon(bpy.types.Operator):
    """Sets selected icon name as icon for the rule creation form."""
    bl_idname = 'blint.select_icon'
    bl_label = 'Select Icon'
    bl_options = {'REGISTER', 'UNDO'}

    attr_name: bpy.props.StringProperty(name='Form attribute', default='')
    """Name of LintRule attribute (which must be a `bpy.props.StringProperty`) to set icon name to."""
    selected_icon: bpy.props.StringProperty(name='Selected Icon', default='')
    """Icon name to be set to the attribute."""

    @classmethod
    def description(cls, context, properties):
        """Uses icon name as part of tooltip."""
        return 'Select "{}" as the {}'.format(format_icon_name(properties.selected_icon), format_icon_name(properties.attr_name))

    def execute(self, context):
        window_manager = context.window_manager
        form_rule = window_manager.blint_form_rule
        try:
            setattr(form_rule, self.attr_name, self.selected_icon)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}


class BT_OT_IconSelection(bpy.types.Operator):
    """Previews icons that can be selected for new rule."""
    bl_idname = 'blint.icon_selection'
    bl_label = 'Select Icon, then press \'OK\' to select'
    bl_description = 'Shows a list of icons to select'
    bl_options = {'REGISTER'}

    attr_filter: bpy.props.StringProperty(name='Search',
                                          description='Filter icons by name',
                                          default='')
    attr_name: bpy.props.StringProperty(name='Form attribute', default='')

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        curr_selected_icon = getattr(wm.blint_form_rule, self.attr_name)

        layout.prop(self, 'attr_filter', text='Search and press Enter')
        layout.label(text='Selected icon: {}'.format(format_icon_name(curr_selected_icon)),
                     icon=curr_selected_icon)

        filtered_icons = get_icons()
        if self.attr_filter:
            filtered_icons = [icon for icon in filtered_icons if self.attr_filter.lower() in icon.lower()]

        row = layout.row(align=True)
        row.alignment = 'CENTER'
        col_idx = 0
        for icon in filtered_icons:
            op = row.operator(BT_OT_SelectIcon.bl_idname, text='', icon=icon,
                              emboss=curr_selected_icon == icon,
                              depress=curr_selected_icon == icon)
            op.attr_name = self.attr_name
            op.selected_icon = icon
            col_idx += 1
            if col_idx == self.num_cols:
                row = layout.row(align=True)
                row.alignment = 'CENTER'
                col_idx = 0

        if col_idx != 0 and col_idx != self.num_cols:
            for _ in range(self.num_cols - col_idx):
                row.label(text="", icon='BLANK1')

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        self.num_cols = 32
        POPUP_PADDING = 10
        WIN_PADDING = 32
        ICON_SIZE = 20
        menu_width = int(min(self.num_cols * ICON_SIZE + POPUP_PADDING, context.window.width - WIN_PADDING))
        return context.window_manager.invoke_props_dialog(self, width=menu_width)
