
from utilities.common import Common
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image


class SageContent(Screen):
    pass


class SageApp(MDApp, Common):
    def __init__(self):
        super().__init__()

# ############################################################## sections overview

    def get_section_overview(self, section_nm):
        self.root.ids.screen_manager.current = 'generic_screen'
        self.root.ids.section_overview.clear_widgets()
        assets_path = self.get_assets_path(section_nm)
        img = Image(source=assets_path, allow_stretch=True)
        self.root.ids.section_overview.add_widget(img)

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

