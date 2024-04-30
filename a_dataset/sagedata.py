
from a_dataset.dataset_shopping import ShoppingData
from a_dataset.dataset_email import EmailData
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial


class SageDataContent(Screen):
    pass


class SageDataApp(MDApp, ShoppingData, EmailData):
    def __init__(self):
        super().__init__()

# ############################################################## populate dataset tabs

    def populate_chosen_dataset_sections(self, dataset_name):
        """
        :param dataset_name: the name of dataset (e.g. shopping)
        :return:
            - transitions to dataset-screen and clears the tabs if exists
            - populates the first 2 tabs; default tab is the activity tab which has a title
            - calls the function to populates the data generation tab
            - when all done switches to default tab
        """
        self.dataset_name = dataset_name
        self.root.ids.screen_manager.current = 'dataset_screen'
        self.root.ids.dataset_tabs.clear_tabs()
        for index, section in enumerate(['activity', 'diagram']):
            tab = TabbedPanelItem(
                text=section, color=[215 / 255, 163 / 255, 9 / 255], background_down=''
            )
            parent_widget = BoxLayout(orientation='vertical', spacing='10sp')
            if section == 'activity':
                s_label = MDLabel(
                    text=f'{self.dataset_name} {section}', halign='center', theme_text_color='Custom',
                    text_color=[81 / 255, 81 / 255, 81 / 255], font_style='H4', size_hint=[1, 0.1]
                )
                parent_widget.add_widget(s_label)
            s_img = Image(source=self.get_assets_path(f'sage_1_dataset/{self.dataset_name}_{section}.png'), allow_stretch=True)
            parent_widget.add_widget(s_img)
            tab.add_widget(parent_widget)
            self.root.ids.dataset_tabs.add_widget(tab)
        gen_tab = TabbedPanelItem(text='generate', color=[215 / 255, 163 / 255, 9 / 255], background_down='')
        gen_tab_widgets = self.get_dataset_generate_tab_widgets()
        gen_tab.add_widget(gen_tab_widgets)
        self.root.ids.dataset_tabs.add_widget(gen_tab)
        self.root.ids.dataset_tabs.switch_to(self.root.ids.dataset_tabs.tab_list[2])

# ############################################################## populate data generation tab

    def get_dataset_generate_tab_widgets(self):
        """
        :return:
            - populates data-size input box, generate button and database-schema
            - binds generate button to a function to return the saved data info
        """
        gen_parent_widget = BoxLayout(orientation='vertical', spacing='10sp')
        gen_top_widget = GridLayout(rows=1, size_hint=[1, 0.15], padding='5sp', spacing='5sp')
        gen_bottom_widget = BoxLayout(orientation='vertical')
        row_input = MDTextFieldRect(
            multiline=False, cursor_color=[196 / 255, 204 / 255, 217 / 255], font_size='18sp', background_normal='',
            hint_text='how many rows of data? (20-5000)', foreground_color=[196 / 255, 204 / 255, 217 / 255],
            background_color=[90 / 255, 101 / 255, 108 / 255]
        )
        gen_top_widget.add_widget(row_input)
        gen_button = Button(
            text='generate data', color='323232', size_hint=[0.3, 1], font_size='18sp', background_normal='',
            background_color=[131 / 255, 173 / 255, 160 / 255]
        )
        gen_button.bind(
            on_release=partial(self.df_to_file_save_generated_data, row_input, gen_bottom_widget)
        )
        gen_top_widget.add_widget(gen_button)
        gen_parent_widget.add_widget(gen_top_widget)
        gen_schema = Image(source=self.get_assets_path(f'sage_2_db/db_schema_{self.dataset_name}.png'), allow_stretch=True)
        gen_bottom_widget.add_widget(gen_schema)
        gen_parent_widget.add_widget(gen_bottom_widget)
        return gen_parent_widget

    def df_to_file_save_generated_data(self, *args):
        """
        :param args: args[0] is the given data size, args[1] is the bottom widget that has db_schema
        :return:
            - if given data size throws error, uses default data size of 12 rows
            - by calling the master dataset dictionary, fetches the dataset generation function
            - calls chosen dataset generate function to create synthetic data
            - after data is generated, removes db_schema image and adds saved data info
        """
        given_data_size = args[0].text
        try:
            self.sage_dataset_size = int(given_data_size)
        except ValueError:
            print('setting default data size of 12')
        gen_bottom_widget = args[1]
        df = self.generate_dataset().get(self.dataset_name)()
        lb_info = MDLabel(
            text=f"{self.dataset_name} dataset size: {print(df) if df is None else df.shape}\n"
                 f"data files are saved in directory: {self.generated_data_path.split(self.app_nm)[1]}",
            font_style='H6', padding='30sp'
        )
        gen_bottom_widget.clear_widgets()
        gen_bottom_widget.add_widget(lb_info)

    def generate_dataset(self):
        d = {
            'shopping': self.generate_shopping_data,
            'email': self.generate_email_data
        }
        return d

# ############################################################## base

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Dataset'
        return SageDataContent()


if __name__ == '__main__':
    SageDataApp().run()







