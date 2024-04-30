
from utilities.db_engines import DatabaseEngines
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial


class SageDBContent(Screen):
    pass


class SageDBApp(MDApp, DatabaseEngines):
    def __init__(self):
        super().__init__()

# ############################################################## engine button sub-items

    def list_db_home_engines(self):
        """
        :return:
            - fetches the list of available database engines from common
            - binds a generic function to each engine to populate the widgets
        """
        parent_btn = self.root.ids.db_home_engine_list
        sub_item_list = self.get_sub_item_list().get('engine').get('sub_item_list')
        dropdown = DropDown()
        for sub_item in sub_item_list:
            print(sub_item)
            btn = Button(
                text=sub_item, color='gray', font_size='20sp', size_hint_y=None,
                background_normal='', background_color='e0e0e0'
            )
            btn.bind(on_press=partial(self.populate_sage_db_screen, btn, dropdown))
            dropdown.add_widget(btn)
        self.selection_dropdown(parent_btn, dropdown)

# ############################################################## database screen widgets

    def populate_sage_db_screen(self, *args):
        """
        :param args: args[0] is the chosen engine, args[1] is the dropdown object
        :return:
            - calls a function from common to updates the global engine name
            - closes the dropdown
            - calls a function to fetch the engine widgets and populates the db_screen
        """
        engine_name, engine_dropdown = args[0].text, args[1]
        self.selected_db_engine(engine_name)
        engine_dropdown.clear_widgets()
        engine_dropdown.dismiss()
        self.root.ids.db_widget.clear_widgets()
        db_screen_engine_widget = self.get_engine_widget()
        self.root.ids.db_widget.add_widget(db_screen_engine_widget)

    def get_engine_widget(self):
        self.root.ids.screen_manager.current = 'db_screen'
        parent_widget = BoxLayout(orientation='vertical', padding=[0, 20, 0, 0])
        btn = Button(
            text=f'create {self.engine} database', color=[0, 0, 0], font_size='20sp',
            size_hint=[0.5, 0.15], pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='', background_color=[131/255, 173/255, 160/255]
        )
        btn.bind(on_release=partial(self.create_db_engine, parent_widget))
        parent_widget.add_widget(btn)
        img = Image(source=f'{self.path_to_assets}/sage_2_db/db_schema_shopping.png', allow_stretch=True)
        parent_widget.add_widget(img)
        return parent_widget

# ############################################################## call to create database

    def create_db_engine(self, *args):
        """
        :param args: args[0] is the db_screen parent widget
        :return:
            - calls a function from db_engines to create respective database
            - adds a text widget to show the outcome of the call (path to db or error)
        """
        parent_widget = args[0]
        parent_widget.clear_widgets()
        try:
            self.dict_engines_functions().get(self.engine)[0]()
            engine_dir = self.get_sub_item_list().get('engine').get('engine_dir').get(self.engine)
            lbd = MDLabel(
                text=f"{self.engine} database is created in directory: \n{engine_dir}",
                font_style='H5', halign='center', padding=[100, 0, 0, 400]
            )
        except Exception as e:
            print(e)
            lbd = MDLabel(text=f"error while creating {self.engine} database", font_style='H5', halign='center')
        parent_widget.add_widget(lbd)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Database'
        return SageDBContent()


if __name__ == '__main__':
    SageDBApp().run()







