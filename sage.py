
from utilities.common import Common
from sections.a_dataset import Dataset
from sections.b_database import Database
from sections.c_insights import Insights
from sections.d_patterns import Patterns
from sections.e_solutions import Solutions
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from functools import partial
from kivy.clock import Clock


class SageContent(Screen):
    pass


class SageApp(MDApp, Common, Dataset, Database, Insights, Patterns, Solutions):
    """
        populating the widgets in each of the 5 sections of Datanota sage-data360 app
    """
    def __init__(self):
        super().__init__()
        self.insights_total_questions = 20

# ############################################################## dataset section

    def get_dataset_widgets(self):
        self.root.ids.screen_manager.current = 'data_home'
        self.root.ids.dataset_box.clear_widgets()
        dataset_home_panel = self.get_generic_tab_panel(total_tabs=3)
        self.root.ids.dataset_box.add_widget(dataset_home_panel)
        dataset_home_panel.clear_tabs()
        for index, section in enumerate(['activity', 'diagram']):
            tab = self.get_dataset_attributes_tabs(
                sage_theme_dict=self.dict_sage_theme_colors(), data_name=self.data_name,
                section=section, img_source=self.get_assets_path(f'{self.data_name}_{section}.png')
            )
            dataset_home_panel.add_widget(tab)
        gen_tab = self.get_generate_dataset_widgets(
            sage_theme_dict=self.dict_sage_theme_colors(), db_schema_path=self.get_assets_path('db_schema_shopping.png'),
            data_name=self.data_name, generated_data_path=self.generated_data_path
        )
        dataset_home_panel.add_widget(gen_tab)
        dataset_home_panel.switch_to(dataset_home_panel.tab_list[2])

# ############################################################## database section

    def get_db_widgets(self):
        self.root.ids.screen_manager.current = 'db_home'
        self.root.ids.db_widget.clear_widgets()
        btn, img, info_widget = self.db_widgets(
            sage_theme_dict=self.dict_sage_theme_colors(),
            img_source=self.get_assets_path('db_schema_shopping.png')
        )
        btn.bind(on_release=partial(self.create_db,  f'{self.db_path}shopping.db', self.generated_data_path, info_widget))
        self.root.ids.db_widget.add_widget(btn)
        self.root.ids.db_widget.add_widget(img)
        self.root.ids.db_widget.add_widget(info_widget)

# ############################################################## insights section Q & A

    def get_insights_widgets(self):
        total_tabs = self.insights_total_questions + 1
        self.root.ids.screen_manager.current = 'insights_home'
        self.root.ids.insights_box.clear_widgets()
        insights_home_panel = self.get_generic_tab_panel(total_tabs=total_tabs)
        self.root.ids.insights_box.add_widget(insights_home_panel)
        insights_home_panel.clear_tabs()
        default_tab = self.get_db_default_tab(
            sage_theme_dict=self.dict_sage_theme_colors(),
            img_source=self.get_assets_path('db_schema_shopping.png')
        )
        insights_home_panel.add_widget(default_tab)
        insights_home_panel.switch_to(insights_home_panel.tab_list[0])
        for num in range(1, total_tabs):
            q = f"q{num}"
            tab = self.populate_insights_questions_tabs(
                sage_theme_dict=self.dict_sage_theme_colors(),
                db_path=self.db_path, num=num, q=q,
                tip_dialog=self.tip_dialog, theme_cls=self.theme_cls
            )
            insights_home_panel.add_widget(tab)

# ############################################################## patterns section

    def pattern_section_layout(self):
        self.root.ids.screen_manager.current = 'patterns_home'
        self.root.ids.patterns_box.clear_widgets()
        pattern_home_label = self.get_patterns_home_label(sage_theme_dict=self.dict_sage_theme_colors())
        self.root.ids.patterns_box.add_widget(pattern_home_label)
        pattern_home_panel = self.get_generic_tab_panel(total_tabs=3)
        self.root.ids.patterns_box.add_widget(pattern_home_panel)
        pattern_home_panel.clear_tabs()
        Clock.schedule_once(partial(self.get_patterns_widgets, pattern_home_panel, pattern_home_label))

    def get_patterns_widgets(self, *args):
        pattern_home_panel = args[0]
        pattern_home_label = args[1]
        pattern_types = list(self.dict_pattern_sections().keys())
        for pattern_type in enumerate(pattern_types):
            tab = self.get_pattern_tabs(
                sage_theme_dict=self.dict_sage_theme_colors(),
                pattern_type=pattern_type[1]
            )
            pattern_home_panel.add_widget(tab)
        pattern_home_panel.bind(current_tab=partial(self.pattern_visual, pattern_home_label))

    def pattern_visual(self, pattern_home_label, instance, value):
        self.root.ids.patterns_box.remove_widget(pattern_home_label)
        if value:
            current_tab = instance.current_tab
            bottom_box = current_tab.content.children[0]
            current_tab_name = current_tab.text
            button = bottom_box.children[1].children[3]
            button.bind(on_press=partial(self.create_pattern_visual, current_tab_name, bottom_box))

    def create_pattern_visual(self, current_tab_name, bottom_box, instance):
        try:
            visual_x_y = self.selected_pattern_visual[0].split(' ')
            x = visual_x_y[0]
            y = visual_x_y[2]
            print(f'======== the list: {visual_x_y}')
            print(f'====== now x and y are: {x}, {y}')
            self.dict_pattern_sections().get(current_tab_name).get('tab_visual')(
                self.path_to_assets, self.shopping_df, x, y
            )
            pattern_img_source = f"{self.path_to_assets}sage_pattern_{current_tab_name.lower()}_{x}_{y}.png"
            for widget in bottom_box.children:
                bottom_box.remove_widget(widget) if isinstance(widget, Image) else print('')
            pattern_image = Image(source=pattern_img_source, allow_stretch=True)
            bottom_box.add_widget(pattern_image)
            pattern_image.reload()
        except Exception as e:
            print(f'========= pattern error: {e}')

# ############################################################## solutions section

    def get_solutions_widgets(self):
        self.root.ids.screen_manager.current = 'solutions_home'
        solution_note = self.solutions_home_buttons(text='database tools', sage_theme_dict=self.dict_sage_theme_colors())
        self.root.ids.solutions_home_layout.add_widget(solution_note)

# ############################################################## generic

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'sage-data360'
        return SageContent()


if __name__ == '__main__':
    SageApp().run()
