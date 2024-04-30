
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import webbrowser
import subprocess
import datetime
import os
import string
import time


class Common:
    def __init__(self):
        self.app_nm = 'sage'
        self.project_path = os.getcwd().split(self.app_nm)[0]
        self.generated_data_path = f'{self.project_path}{self.app_nm}/a_dataset/data_files/'
        self.dataset_name = ''
        self.sage_dataset_size = 12
        self.db_path = f'{self.project_path}{self.app_nm}/b_database/databases/'
        self.hadoop_sbin_path = '/usr/local/Cellar/hadoop/3.3.1/libexec/sbin/'
        self.hdfs_hive_path = 'hdfs://localhost:9000/user/hive/warehouse/'
        self.path_to_assets = f'{self.project_path}{self.app_nm}/utilities/assets/'
        self.saved_queries_path = f'{self.project_path}{self.app_nm}/c_insight/saved_data/'
        self.sage_solution_path = self.get_assets_path('sage_5_solution/')
        self.letters = list(string.ascii_lowercase)
        self.engine_type = 'rdbms'
        self.engine = 'sqlite'
        self.prototype_nm = ''
        self.all_prototypes = ['Amber', 'Quartz', 'Granite']

# ############################################################### window screenshot

    @staticmethod
    def sage_window_ss(img_nm):
        Window.screenshot(name=img_nm)

# ############################################################### current year

    @staticmethod
    def get_current_year(additional_text):
        current_year = datetime.datetime.now().year
        if additional_text == '':
            returned_year = current_year
        else:
            returned_year = f'{current_year} {additional_text}'
        return returned_year

# ############################################################### path to assets

    def get_assets_path(self, additional_path):
        assets_path = f'{self.project_path}sage/utilities/assets/'
        if additional_path == '':
            returned_path = assets_path
        else:
            returned_path = f'{assets_path}{additional_path}'
        return returned_path

# ############################################################### create directory if not exists

    @staticmethod
    def create_dir_if_not_exists(path_to_dir):
        os.makedirs(path_to_dir) if not os.path.exists(path_to_dir) \
            else print(f"Directory '{path_to_dir}' already exists.")

# ############################################################## demo

    @staticmethod
    def dn_sage_demo():
        webbrowser.open('https://www.datanota.com/sage')

# ############################################################### navbar top-right tip

    @staticmethod
    def tip_dialog(*args):
        title = args[0]
        tip = args[1]
        dialog = MDDialog(
            title=title,
            text='[color=222222]' + tip,
            buttons=[
                MDFlatButton(
                    text='Dismiss',
                    theme_text_color='Custom',
                    text_color=args[2],
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

# ############################################################## engine settings

    def selection_dropdown(self, *args):
        parent_button = args[0]
        if args[1] == 'navbar':
            dropdown = DropDown()
            sub_item_list = self.get_sub_item_list().get(parent_button.text).get('sub_item_list')
            for sub_item in sub_item_list:
                btn = self.nav_bar_dropdown_parent(sub_item, parent_button, dropdown)
                dropdown.add_widget(btn)
        else:
            dropdown = args[1]
        dropdown.open(parent_button)

    def nav_bar_dropdown_parent(self, *args):
        sub_item = args[0]
        parent_button = args[1]
        dropdown = args[2]
        btn = Button(text=sub_item, size_hint_y=None, height=60)
        btn.bind(on_release=lambda x: self.selected_sub_item(parent_button, x.text, dropdown))
        return btn

    def selected_sub_item(self, *args):
        parent_button, text, dropdown = args[0], args[1], args[2]
        self.get_sub_item_list().get(parent_button.text).get('action')(text)
        dropdown.dismiss()

    def get_sub_item_list(self):
        d = {
            'window_size': {
                'sub_item_list': ['default', 'large'],
                'action': self.selected_window_size
            },
            'engine': {
                'sub_item_list': ['SQLite', 'Apache-Hive', 'PostgreSQL', 'MongoDB', 'Neo4J'],
                'action': self.selected_db_engine,
                'engine_dir': {
                    'sqlite': 'sage/b_database/databases',
                    'apache-hive': 'path-to-hdfs/user/hive/warehouse'
                }
            },
            'dataframe': {
                'sub_item_list': ['pandas', 'pyspark'],
                'action': print('======')
            }
        }
        return d

# ############################################################## window size settings

    @staticmethod
    def selected_window_size(size):
        # for size in self.get_sub_item_list().get('window_size').get('sub_item_list'):
        if size == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)

# ############################################################## database engine settings

    def selected_db_engine(self, engine):
        self.engine = engine.lower()

# ############################################################### chmod

    @staticmethod
    def chmod_directory(path_to_directory, mode):
        subprocess.run(
            ['hdfs', 'dfs', '-chmod', '-R', mode, path_to_directory],
            check=True, text=True, capture_output=True
        )


