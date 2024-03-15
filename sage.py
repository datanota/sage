
from utilities.common import Common
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


class SageContent(Screen):
    pass


class SageApp(MDApp, Common):
    def __init__(self):
        super().__init__()

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ##############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE: data-360'
        return SageContent()


if __name__ == '__main__':
    SageApp().run()







