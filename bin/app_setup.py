
import hook_system_variables as app
import os_operations as op
import os


home_dir = op.get_home()
app_tree = home_dir+app.data_storage_path
if not os.path.exists(app_tree):
    op.create_tree(app_tree)
