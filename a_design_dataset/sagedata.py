
from a_design_dataset.data_files.data_generation import DataGeneration
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
import webbrowser
import datetime


class SageDataContent(Screen):
    pass


class SageDataApp(MDApp, DataGeneration):
    def __init__(self):
        super().__init__()
        self.q = ''
        self.q_re_run = ''
        self.response_input = None
        self.r_box = BoxLayout(orientation='vertical')

# ############################################################## data generation
    def data_input_check(self):
        c = self.root.ids.num_customers.text
        p = self.root.ids.num_products.text

        lbc = MDLabel(text=f'Total number of customers: {c}', font_size='40sp')
        lbp = MDLabel(text=f'Total number of products: {p}', font_size='40sp')

        btn = Button(
                text='save data', color='000000', font_size='20sp', background_color='85ADA3',
                background_normal='', size_hint=(0.9, 0.75)
            )
        self.root.ids.data_input_check.clear_widgets()
        self.root.ids.data_input_check.add_widget(lbc)
        self.root.ids.data_input_check.add_widget(lbp)
        self.root.ids.data_input_check.add_widget(btn)
        btn.bind(on_press=partial(self.save_to_file_generated_data, c, p))

    def save_to_file_generated_data(self, *args):
        cust_num = args[0]
        prd_num = args[1]
        self.generate_data(cust_num, prd_num)
        lbd = MDLabel(
            text=f"data is saved in dir: {self.generated_data_path.split('sage')[1]}",
            font_size='80sp'
        )
        self.root.ids.data_preview.add_widget(lbd)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ##############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Generate Data'
        return SageDataContent()


if __name__ == '__main__':
    SageDataApp().run()







