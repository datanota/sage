
from b_create_database.database.create_database import CreateDatabase
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen


class SageDBContent(Screen):
    pass


class SageDBApp(MDApp, CreateDatabase):
    def __init__(self):
        super().__init__()
        self.q = ''
        self.q_re_run = ''
        self.response_input = None
        self.r_box = BoxLayout(orientation='vertical')

# ############################################################## build a database

    def create_database(self):
        self.df_to_db()
        lbd = MDLabel(
            text=f"database is created: {self.db_path.split('sage')[1]}",
            font_size='80sp'
        )
        self.root.ids.db_outcome.clear_widgets()
        self.root.ids.db_outcome.add_widget(lbd)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ##############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Create Database'
        return SageDBContent()


if __name__ == '__main__':
    SageDBApp().run()







