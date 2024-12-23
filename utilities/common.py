
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import MDFlatButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
import pandas as pd
import webbrowser
import datetime
import os


class Common:
    def __init__(self):
        super().__init__()
        self.app_nm = 'sage'
        self.project_path = os.getcwd().split(self.app_nm)[0]
        self.generated_data_path = f'{self.project_path}{self.app_nm}/data/'
        self.data_name = 'shopping'
        self.db_path = f'{self.project_path}{self.app_nm}/data/'
        self.shopping_df = pd.read_csv(f"{self.generated_data_path}{self.data_name}.csv")
        self.path_to_assets = f'{self.project_path}{self.app_nm}/utilities/assets/'

# ############################################################### sage custom theme RGB colors

    @staticmethod
    def dict_sage_theme_colors():
        return {
            'app_background': [212 / 255, 213 / 255, 212 / 255],
            'app_text': [81 / 255, 81 / 255, 81 / 255],
            'app_button_background': [131 / 255, 173 / 255, 160 / 255],
            'app_button_text': [0, 0, 0],
            'dn_gold': [215 / 255, 163 / 255, 9 / 255],
            'input_box_background': [90 / 255, 101 / 255, 108 / 255],
            'input_box_hint': [158 / 255, 158 / 255, 158 / 255],
            'input_box_foreground': [1, 1, 1]
        }

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

# ############################################################## demo

    @staticmethod
    def dn_sage_demo():
        webbrowser.open('https://www.datanota.com/data-360')

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

# ############################################################## dropdown settings

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
        return {
            'window size': {
                'sub_item_list': ['default', 'large'],
                'action': self.selected_window_size
            }
        }

# ############################################################## window size settings

    @staticmethod
    def selected_window_size(size):
        if size == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)

# ############################################################## generic widgets

    def get_generic_tab_panel(self, total_tabs):
        return TabbedPanel(
            tab_width=Window.width / total_tabs, do_default_tab=False, tab_pos='bottom_mid',
            background_image='', background_color=self.dict_sage_theme_colors().get('app_background')
        )
