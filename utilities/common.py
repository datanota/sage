
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy as np
import webbrowser
import datetime
import os
import string


class Common:
    def __init__(self):
        self.app_nm = 'SAGE'
        self.project_path = os.getcwd().split('sage')[0]
        self.generated_data_path = f'{self.project_path}sage/a_design_dataset/data_files/'
        self.db_path = f'{self.project_path}sage/b_create_database/database/'
        self.saved_queries_path = f'{self.project_path}sage/c_insights/queries/saved/'
        self.numbers = list(np.arange(10))
        self.age_group = list(np.arange(15, 91))
        self.letters = list(string.ascii_lowercase)
        self.prefix = ['Mc', 'Ash', 'Ban', 'Fitz', 'De', 'Nin', 'El']
        self.location_list = ['Paris, France', 'Milan, Italy', 'LA, USA', 'Madrid, Spain', 'San Jose, USA']
        self.price = list(np.arange(0, 100, 0.1))
        self.quantity = list(range(0, 1000))
        self.start = '2022-01-01'
        self.end = '2023-12-30'

# ############################################################### screenshot

    @staticmethod
    def sage_ss():
        img_nm = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        Window.screenshot(name=img_nm + '.png')

# ############################################################## demo

    @staticmethod
    def dn_sage_demo():
        webbrowser.open('https://www.datanota.com/sage')

# ############################################################### navbar top-right tip

    def tip_dialog(self, *args):
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

    @staticmethod
    def window_size_settings(size):
        if size == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)





