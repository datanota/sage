
from assets.patterns_analytics import PattersAnalytics
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen


class SagePatternsContent(Screen):
    pass


class NumNum(Screen):
    pass


class NumCat(Screen):
    pass


class CatCat(Screen):
    pass


class Com_Met(Screen):
    pass


class SagePatternsApp(MDApp, PattersAnalytics):
    def __init__(self):
        super().__init__()

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ##############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Patterns'
        return SagePatternsContent()


if __name__ == '__main__':
    SagePatternsApp().run()







