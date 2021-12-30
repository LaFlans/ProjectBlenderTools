import bpy
import os
from bpy.types import Menu, Operator, Panel
from bpy.props import StringProperty

bl_info = {
    "name": "FBX File Updater",
    "author": "Flan",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3Dビュー > ツールシェルフ",
    "support": "TESTING",
    "description": "Update FBX File",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

# ファイルブラウザを表示
class ShowFileBrowser(Operator):
    bl_idname = "object.show_file_browser"
    bl_label = "ファイルブラウザ"
    bl_description = "ファイルブラウザを開きます"
    bl_options = {'REGISTER', 'UNDO'}

    # 指定のファイル形式のみ表示
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    # ファイル情報を保存する為に必要な変数を定義
    filepath: StringProperty(subtype="FILE_NAME")
    filename: StringProperty()
    directory: StringProperty(subtype="FILE_NAME")

    def execute(self, context):
        self.report({'INFO'}, "[FilePath] %s, [FileName] %s, [Directory] %s" % (self.filepath, self.filename, self.directory))

        # 対象のファイルパスを保存
        bpy.types.Scene.fbx_file_path = self.filepath

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)

        return {'RUNNING_MODAL'}

# FBXファイルを更新するオペレータ
class UpdateFbxFile(Operator):

    bl_idname = "object.create_object"
    bl_label = "FBXファイル更新"
    bl_description = "最後に保存したFBXファイルを更新します"
    bl_options = {'REGISTER', 'UNDO'}

    comment: StringProperty(default="FBXファイルを更新したよ！", options={'HIDDEN'})

    # メニューを実行したときに呼ばれる関数
    def execute(self, context):
        if not os.path.exists(str(bpy.types.Scene.fbx_file_path)):
            self.report({'ERROR'}, "有効なファイルパスが設定されていません")
            return {'FINISHED'}

        # 現在はデフォルトの設定で保存しています
        bpy.ops.export_scene.fbx(filepath=bpy.types.Scene.fbx_file_path)

        self.report({'INFO'}, self.comment)

        return {'FINISHED'}

class VIEW3D_PT_CustomPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FBXFileUpdater"
    bl_label = "FBXFileUpdater"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="対象のファイルを選択")
        layout.operator(ShowFileBrowser.bl_idname, text=context.scene.fbx_file_path)
        layout.operator(UpdateFbxFile.bl_idname, text="FBXファイル更新")

# メニューを構築する関数
def menu_fn_1(self, context):
    self.layout.operator(VIEW3D_PT_CustomPanel.bl_idname, text="項目 2", icon='PLUGIN')

# Blenderに登録するクラス
classes = [
    UpdateFbxFile,
    VIEW3D_PT_CustomPanel,
    ShowFileBrowser,
]

# プロパティ削除
def clear_prop():
    del bpy.types.Scene.fbx_file_path

# アドオン有効化時の処理
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn_1)

    # ファイルパス変数(プロパティ)登録
    bpy.types.Scene.fbx_file_path = StringProperty(default="ファイルを選択してください")
    print("FBXFileUpdaterが有効化されました。")

# アドオン無効化時の処理
def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn_1)

    for c in classes:
        bpy.utils.unregister_class(c)
    print("FBXFileUpdaterが無効化されました。")

    # ファイルパス変数(プロパティ)削除
    clear_prop()

# メイン処理
if __name__ == "__main__":
    register()
